import random
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import Flask, render_template, redirect, url_for, request, flash, logging
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

# Configuring MySQL Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'cross_path_alert'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# Initialise MySQL
mysql = MySQL(app)


@app.route('/')
def home():
	return render_template('home.html')



###################################### primary register form ########################
class RegisterForm(Form):                                                           #
    name = StringField('Name', [validators.Length(min=2, max=50)])                  #
    email = StringField('Email', [validators.Length(min=6, max=50)])                #
    password = PasswordField('Password', [                                          #
            validators.DataRequired(),                                              #
            validators.EqualTo('confirm', message='Passwords do not match')         #
        ])                                                                          #
    confirm = PasswordField('Confirm Password')                                     #
#####################################################################################

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create a connection and initialise a cursor to interface flask, python and mysql
        cur = mysql.connection.cursor()

        # Execute mysql commands
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))

        # Commit to the database
        mysql.connection.commit()

        # Close connection and cursor
        cur.close()

        flash("You are now registered", 'success')

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)



###################################### primary login form ###########################
class LoginForm(Form):                                                              #
    email = StringField('Registered Email', [validators.Length(min=6, max=50)])     #
    password = PasswordField('Password', [validators.DataRequired()])               #
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
                flash("You are now logged in", 'success')
                return redirect(url_for('home'))
            else:
                error = "Invalid Password"
                return render_template("login.html", form=form, error=error)
        else:
            error = "No user with that E-mail ID"
            return render_template("login.html", form=form, error=error)
	
	cur.close()
	return render_template("login.html", form=form)
    return render_template("login.html", form=form)



@app.route("/about/")
def about():
    return render_template('about.html')
  
if __name__ == "__main__":
    app.run(debug=True)    # Remember to remove debug=True in production
