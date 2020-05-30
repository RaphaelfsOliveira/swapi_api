from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    context = {
        'name': 'Raphael',
    }
    return render_template('base.html', **context)