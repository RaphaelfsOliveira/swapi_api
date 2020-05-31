from flask import Flask, request, render_template
from settings import endpoint
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def IndexView():
    try:
        root_api = requests.get(endpoint)
        url = '{}{}'.format(endpoint, 'people/')

        context = {
            'error_title': 'Erro',
            'error_msg': 'Numero máximo de conexões a api excedido' if root_api.status_code != 200 else 'Erro interno'
        }

        if request.method == 'POST':
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
            'pages': {
                'previous': {
                    'url': response.json()['previous'],
                    'page': response.json()['previous'][-1] if response.json()['previous'] else '',
                },
                'next': {
                    'url': response.json()['next'],
                    'page': response.json()['next'][-1] if response.json()['next'] else '',
                },
                'current': int(response.json()['next'][-1]) - 1 if response.json()['next'] else '',
            },
        }
    except Exception:
        pass

    return render_template('index.html', **context)