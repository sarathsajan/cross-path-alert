from flask import Flask
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cross-path-alert'

@app.route('/')
def home():
    return ("<h1>Stay put, Stay Safe</h1>")

if __name__ == "__main__":
    app.run()