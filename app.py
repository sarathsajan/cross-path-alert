import random
from flask import Flask, render_template, redirect, url_for, request

# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

@app.route('/')
@app.route('/index')
@app.route('/home') # change home later when you have a new home.html
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])           # login part can be done better
def login():

    error = ''
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('about'))
    return render_template('login.html', error=error)

@app.route("/about")
def about():
	return render_template('about.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')    

if __name__ == "__main__":
	app.run(debug=True) # Remember to remove debug=True finally!!!
