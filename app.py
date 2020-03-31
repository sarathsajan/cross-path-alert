import random
import data.py
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

database = database()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login/')
def login():
    return render_template('login.html', data=database)

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)    # Remember to remove debug=True in production
