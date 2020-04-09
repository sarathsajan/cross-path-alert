
from data import userdetails
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, session
# A more formal packaging needed... with __init__.py as the development grows.

app = Flask(__name__)
app.config['SECRET_KEY'] = "cross-path-alert"

data = userdetails()


@app.route('/test')
def test():
   return render_template('sarath.html', output_data = data)


if __name__ == "__main__":
    app.run(debug=True)    # Remember to remove debug=True in production 