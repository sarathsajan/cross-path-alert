from flask import Flask, render_template
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cross-path-alert'

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()