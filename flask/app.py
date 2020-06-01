from flask import Flask, request, render_template
from settings import endpoint, search
import requests
import json


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
    
    response = response.json()

    new_starships = []
    starships = response['results']
    for ship in starships:
        
        def is_valid(value):
            if value and value != 'unknown':
                return value
            return None
        
        def calc_score(hyperdrive_rating, cost_in_credits):
            hyperdrive_rating = float(hyperdrive_rating) if is_valid(hyperdrive_rating) else None
            cost_in_credits = float(cost_in_credits) if is_valid(cost_in_credits) else None

            if hyperdrive_rating and cost_in_credits:
                result = (hyperdrive_rating / cost_in_credits) * 1000000
                return '{:.10f}'.format(result)

            return ''
        
        ship['score'] = calc_score(ship['hyperdrive_rating'], ship['cost_in_credits'])

        new_ship = {
            'name': ship['name'],
            'model': ship['model'],
            'score': ship['score'],
            'manufacturer': ship['manufacturer'],
            'cost_in_credits': ship['cost_in_credits'],
            'length': ship['length'],
            'max_atmosphering_speed': ship['max_atmosphering_speed'],
            'crew': ship['crew'],
            'passengers': ship['passengers'],
            'cargo_capacity': ship['cargo_capacity'],
            'consumables': ship['consumables'],
            'hyperdrive_rating': ship['hyperdrive_rating'],
            'MGLT': ship['MGLT'],
            'starship_class': ship['starship_class'],
        }
        new_starships.append(new_ship)
    
    response['results'] = new_starships
    data = json.dumps(response)

    context = {
        'data': data,
        'pages': {
            'previous': {
                'url': response['previous'],
                'page': response['previous'][-1] if response['previous'] else '',
            },
            'next': {
                'url': response['next'],
                'page': response['next'][-1] if response['next'] else '',
            },
            'current': int(response['next'][-1]) - 1 if response['next'] else '',
        },
    }
    return render_template('starships_page.html', **context)