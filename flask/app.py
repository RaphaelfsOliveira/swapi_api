from flask import Flask, request, render_template
from settings import endpoint
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def IndexView():
    root_api = requests.get(endpoint)

    if request.method == 'POST':
        if request.form:
            url_category = request.form['select_category']
            response = requests.get(url_category)
    else:    
        url = '{}{}'.format(endpoint, 'people/')
        response = requests.get(url)

    context = {
        'data': response.text,
        'root_api': root_api.json()
    }
    return render_template('index.html', **context)