from flask import Flask, render_template,redirect, url_for, request
import random

app = Flask(__name__)

@app.route("/")

def main():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])           #login part can be done better

def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('one'))
    return render_template('login.html', error=error)


@app.route("/about")
def about():
   return render_template('about.html')




if __name__ == "__main__":
    app.run(debug=True)