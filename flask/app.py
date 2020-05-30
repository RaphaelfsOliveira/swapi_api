from flask import Flask
from flask import render_template
from settings import endpoint
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def IndexView():
    url = '{}/{}'.format(endpoint, 'people/1/')
    
    response = requests.get(url)
    
    context = {
        'name': 'Test Nome',
        'data': response
    }
    return render_template('index.html', **context)