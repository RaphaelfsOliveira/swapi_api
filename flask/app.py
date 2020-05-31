from flask import Flask, request, render_template
from settings import endpoint, search
import requests


app = Flask(__name__)

def error_log(response):
    return {
        'error_title': 'Erro',
        'error_msg': 'Numero máximo de conexões a api excedido' if response.status_code != 200 else 'Erro interno'
    }


@app.route('/', methods=['GET', 'POST'])
def IndexView():
    try:
        root_api = requests.get(endpoint)
        url = '{}{}'.format(endpoint, 'people/')

        context = error_log(root_api)

        if request.method == 'POST':
            if 'select_category' in request.form:
                url_category = request.form['select_category']

                if 'search_input' in request.form:
                    search_input = request.form['search_input']

                    response = requests.get(url_category + search.format(search_input))
                else:
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


@app.route('/starships', methods=['GET', 'POST'])
def StarshipsView():
    url = '{}{}'.format(endpoint, 'starships/')

    if request.method == 'POST':
        if 'pagination' in request.form:
            page = request.form['pagination']
            response = requests.get(page)
    else:
        response = requests.get(url)
    
    context = error_log(response)

    context = {
        'data': response.text,
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
    return render_template('starships_page.html', **context)