from config import AppData
import datetime
from math import radians, cos, sin, asin, sqrt
from functools import wraps
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from wtforms import Form, StringField, BooleanField, DateTimeField, PasswordField, validators
from flask import Flask, render_template, redirect, url_for, request, flash, session
# A more formal packaging needed... with __init__.py as the development grows.

appdata = AppData()

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"
app.config.from_pyfile('config.cfg')

# Configuring MySQL Database
app.config['MYSQL_HOST'] = 'localhost'                                                  # localhost
#app.config['MYSQL_HOST'] = 'amisafe.mysql.pythonanywhere-services.com'                  # amisafe
app.config['MYSQL_USER'] = 'root'                                                       # localhost
#app.config['MYSQL_USER'] = 'amisafe'                                                    # amisafe
app.config['MYSQL_PASSWORD'] = appdata['database-password']                                                  # localhost
#app.config['MYSQL_PASSWORD'] = appdata['database-password']                                             # amisafe
app.config['MYSQL_DB'] = 'cross_path_alert'                                             # localhost
#app.config['MYSQL_DB'] = 'amisafe$amisafe'                                                      # amisafe
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#app.config['MYSQL_PORT'] = 3306                                                         # while not in localhost

mail = Mail(app)
mysql = MySQL(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    reg_users = cur.execute("SELECT * FROM users")
    cur.close()
    return render_template('home.html', reg_users=reg_users)



@app.route("/about/")
def about():
    return render_template('about.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised, please log in", 'danger')
            return redirect(url_for('login'))
    return wrap

def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised, please log in", 'danger')
            return redirect(url_for('adminlogin'))
    return wrap

def send_confirmation_email(email):
    token = s.dumps(email, salt=appdata['salt-email-confirm'])
    msg = Message('Verification e-mail', sender='amisafe2help@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = "This is your verification link. It expires in 15 minutes. Click on this verification link to verify your e-mail address \n\n {}".format(link)
    mail.send(msg)


###################################### primary register form ########################
class RegisterForm(Form):                                                           
    name = StringField('Name', [validators.Length(min=2, max=50)])                  
    email = StringField('Email', [
            validators.Length(min=6, max=50),
            validators.Email(message="Enter a valid E-mail ID")
        ])                                                                          
    password = PasswordField('Password', [                                          
            validators.DataRequired(),
            validators.Length(min=8),                                              
            validators.EqualTo('confirm', message='Passwords do not match')         
        ])                                                                          
    confirm = PasswordField('Confirm Password')

    tandc = BooleanField('', [validators.DataRequired()])
#####################################################################################

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        tandc = form.tandc.data

        # Create a connection and initialise a cursor to interface flask, python and mysql
        cur = mysql.connection.cursor()

        # Check if that email is already taken
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if result > 0:
            error = "E-mail already taken"
            return render_template("signup.html", form=form, error=error)

        if tandc:
            # Execute mysql commands
            cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))

            # Commit to the database
            mysql.connection.commit()

            # Close connection and cursor
            cur.close()

            send_confirmation_email(email)
            flash("You are now registered", 'success')
            flash("Your email account is not verified. We have sent a verification link to your registered E-mail", 'warning')

            return redirect(url_for('login'))
        else:
            error = "You need to agree to our Terms and Conditions, Disclaimer"
            return render_template("signup.html", form=form, error=error)
    return render_template('signup.html', form=form)



###################################### primary login form ###########################
class LoginForm(Form):                                                              
    email = StringField('Registered Email', [
        validators.Length(min=6, max=50),
        validators.Email(message="Enter a valid E-mail ID")
    ])
    password = PasswordField('Password', [validators.DataRequired()])               
#####################################################################################

@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate_email = form.email.data
        candidate_password = form.password.data

        # Create a connection and initialise a cursor to interface flask, python and mysql
        cur = mysql.connection.cursor()

        # Execute mysql commands
        # Fetch username from the database
        result = cur.execute("SELECT * FROM users WHERE email = %s", [candidate_email])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(candidate_password, password):
                if data['account_confirmed'] == 1:
                    flash("You are now logged in", 'success')
                    session['logged_in'] = True
                    session['email'] = data['email']
                    session['name'] = data['name']
                    return redirect(url_for('usersdashboard'))
                else:
                    send_confirmation_email(data['email'])
                    error = "Your e-mail account is not verified. We have sent a verification link to your registered e-mail. Please check your e-mail."
                    return render_template("login.html", form=form, error=error)
            else:
                error = "Invalid Password"
                return render_template("login.html", form=form, error=error)
        else:
            error = "No user with that E-mail ID"
            return render_template("login.html", form=form, error=error)
        cur.close()
    return render_template("login.html", form=form)



@app.route('/confirmEmail/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt=appdata['salt-email-confirm'], max_age=900)
    except SignatureExpired:
        return "Token expired. Use the token within 15 minutes."
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET account_confirmed = 1 WHERE email = %s", [email])
    mysql.connection.commit()
    cur.close()

    flash("Your e-mail has been verified", 'success')
    return redirect(url_for('login'))



############################### travel history input form ###########################
class TravelHistoryInputForm(Form):
    date = StringField('Date', [validators.DataRequired()])
    time = StringField('Time', [validators.DataRequired()])
    location = StringField('Enter the coordinates', [
            validators.DataRequired(),
            validators.Length(max=25)
        ])
#####################################################################################

@app.route("/usersdashboard/addData/", methods=['POST', 'GET'])
@is_logged_in
def addUserData():
    form = TravelHistoryInputForm(request.form)
    if request.method == 'POST' and form.validate():

        input_date = form.date.data
        input_time = (form.time.data)+":00"

        temp_input_location = form.location.data            # N10.58662 E076.21988
        try:
            temp_input_location = str(temp_input_location.translate({ord(i): None for i in 'NEne'}))
            input_latitude, input_longitude = temp_input_location.split(' ')
        except Exception as e:
            flash("Invalid coordinates, try using the map given below", "danger")
            return render_template("addUserData.html", form=form)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users_travel_history(email, date, time, latitude, longitude) VALUES(%s, %s, %s, %s, %s)", (session['email'], input_date, input_time, input_latitude, input_longitude))
        mysql.connection.commit()
        cur.close()

        flash("Your travel history has been updated", 'success')

        return redirect(url_for('usersdashboard'))
    return render_template("addUserData.html", form=form)


@app.route("/usersdashboard/")
@is_logged_in
def usersdashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users_travel_history WHERE email = %s", [session['email']])
    user_data = cur.fetchall()
    result = cur.execute("SELECT * FROM patients_travel_history")
    patients_data = cur.fetchall()
    cur.close()

    modified_user_data = []
    for temp in user_data:
        temp['danger_level'] = 0
        modified_user_data.append(temp)    

    #################################### cross match algorithm #####################################
    database = patients_data             # patient data from sql
    userdata = modified_user_data        # users data from sql

    def distance(lat1, lat2, lon1, lon2):
        lon1 = radians(lon1)       #converting radians
        lon2 = radians(lon2) 
        lat1 = radians(lat1) 
        lat2 = radians(lat2) 
            
        dlon = lon2 - lon1         # Haversine formula 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371                     #Radius of earth
        return(c * r)                #final output

    # ITERATE THOUGH PATIENT DATABASE AND CALCULATE PROXIMITY (HEART) #
    def calc_prox(val1,ulat,ulon):
        flag1 = False 
        flag2 = False 
        flag3 = False

        for p in database:    
            pdate = p['date']                 
            ptime = p['time']                 
            checkyear, checkmonth, checkdate = str(pdate).split('-')
            checkhour, checkminutes, _ = str(ptime).split(':')
            val2 = datetime.datetime(int(checkyear),int(checkmonth),int(checkdate),int(checkhour),int(checkminutes),00) # if the person has no account
            #print(val2)                        
            plat = float(p['latitude'])
            plon = float(p['longitude'])
            #plat = float(plat[0 : len(plat)-1])
            #plon = float(plon[0 : len(plon)-1])

            difference = val1 - val2

            time = difference.total_seconds() / 60**2   # time in Hours
            dist = distance(ulat, plat, ulon, plon)     # in kilometers
            #print(dist)
            #print(time)

            if dist < 0.1 and time >= -2 and time <= 4:
                flag1 = True
            elif dist < 0.25 and time >= -4 and time <= 8:
                flag2 = True
            elif dist < 0.5 and time >= -7 and time <= 14:
                flag3 = True

        if flag1 == True:
            return(1)
        elif flag2 == True:
            return(2)
        elif flag3 == True:
            return(3)
        else:
            return(4)



    # FUNCTION FOR ACCOUNT USERS #
    def for_user_with_account():
        temp_dictionary = []
        for u in userdata:                                                    
            udate=u['date']                 
            utime=u['time']                 
            checkyear,checkmonth,checkdate = str(udate).split('-')
            checkhour,checkminutes, _ = str(utime).split(':')
            val1 = datetime.datetime(int(checkyear), int(checkmonth), int(checkdate), int(checkhour), int(checkminutes), 00)
            ulat = float(u['latitude'])
            ulon = float(u['longitude'])
            #ulat=float(ulat[0:len(ulat)-1])
            #ulon=float(ulon[0:len(ulon)-1])
            u['danger_level'] = calc_prox(val1, ulat, ulon)
            temp_dictionary.append(u)
        return temp_dictionary



    modified_user_data = for_user_with_account()         #call for users with account
    risk_flag = 4
    temp_flag = 4
    for i in modified_user_data:
        temp_flag = i['danger_level']
        if temp_flag < risk_flag:
            risk_flag = temp_flag



    return render_template('usersdashboard.html', user_data=modified_user_data, flag=risk_flag)



@app.route("/patientsdashboard/addData/", methods=['POST', 'GET'])
@is_admin_logged_in
def addPatientData():
    form = TravelHistoryInputForm(request.form)
    if request.method == 'POST' and form.validate():

        input_date = form.date.data
        input_time = (form.time.data)+":00"

        temp_input_location = form.location.data            # N10.58662 E076.21988
        try:
            temp_input_location = str(temp_input_location.translate({ord(i): None for i in 'NEne'}))
            input_latitude, input_longitude = temp_input_location.split(' ')
        except Exception as e:
            flash("Invalid coordinates, try using the map given below", "danger")
            return render_template("addPatientData.html", form=form)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients_travel_history(date, time, latitude, longitude) VALUES(%s, %s, %s, %s)", (input_date, input_time, input_latitude, input_longitude))
        mysql.connection.commit()
        cur.close()

        flash("Patients travel history has been updated", 'success')

        return redirect(url_for('patientsdashboard'))
    return render_template("addPatientData.html", form=form)



@app.route("/patientsdashboard/")
@is_admin_logged_in
def patientsdashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM patients_travel_history")
    data = cur.fetchall()
    cur.close()
    return render_template('patientsdashboard.html', patient_data=data)



@app.route("/adminlogin/", methods=['POST', 'GET'])
def adminlogin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate_email = form.email.data
        candidate_password = form.password.data

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM admins WHERE email = %s", [candidate_email])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(candidate_password, password):
                flash("You are now logged in", 'success')
                session['admin_logged_in'] = True
                session['email'] = data['email']
                session['name'] = data['name']

                return redirect(url_for('patientsdashboard'))
            else:
                error = "Invalid Password"
                return render_template("adminlogin.html", form=form, error=error)
        else:
            error = "No user with that E-mail ID"
            return render_template("adminlogin.html", form=form, error=error)
        cur.close()
    return render_template("adminlogin.html", form=form)



@app.route("/logout/")
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for('home'))


  
if __name__ == "__main__":
    app.run(debug=True)    # Remember to remove debug=True in production