from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route('/')
def IndexView():
    context = {
        'name': 'Test Nome',
    }
    return render_template('index.html', **context)