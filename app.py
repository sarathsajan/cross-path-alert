import random
from flask import Flask, render_template, redirect, url_for, request
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login/')
def login():
    return_render_template('login.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)    # Remember to remove debug=True in production