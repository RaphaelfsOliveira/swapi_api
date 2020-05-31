from flask import Flask, request, render_template
from settings import endpoint
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def IndexView():
    root_api = requests.get(endpoint)
    url = '{}{}'.format(endpoint, 'people/')

    if request.method == 'POST':
        print(
            request.form
        )
        if 'select_category' in request.form:
            url_category = request.form['select_category']
            response = requests.get(url_category)
        elif 'pagination' in request.form:
            page = request.form['pagination']
            response = requests.get(page)
        else:
            response = requests.get(url)
    else:    
        response = requests.get(url)

    context = {
        'data': response.text,
        'root_api': root_api.json(),
        'pages': response.json(),
    }
    return render_template('index.html', **context)