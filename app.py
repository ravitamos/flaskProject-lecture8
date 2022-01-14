from flask import Flask, redirect, url_for
from flask import jsonify
from flask import render_template
from flask import request
from flask import session
import mysql.connector
import requests
import random
import asyncio
import aiohttp
from interact_with_db import interact_db

app = Flask(__name__)
app.secret_key = '123'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

users = {'user1': {'name': 'yossi', 'email': 'yo@gmail.com'},
         'user2': {'name': 'ravit', 'email': 'ra@gmail.com'}, 'user3': {'name': 'roi', 'email': 'ro@gmail.com'},
         'user4': {'name': 'lir', 'email': 'li@gmail.com'},
         'user5': {'name': 'shir', 'email': 'sh@gmail.com'}}
username = ''


@app.route('/')
def home_func():  # put application's code here
    # db
    found = False
    if found:
        return render_template('index.html', name='ravit')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_func():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Db
        found = True
        if found:
            session['username'] = username
            return redirect(url_for('home_func'))
        else:
            return render_template('login.html')


@app.route('/assignment8')
def about_func():
    # db
    return render_template('assignment8.html', profile={'name': 'ravit', 'second': 'amos'},
                           university='bgu', fav_movies=['Lion king', 'the Avengers', 'AVATAR'],
                           hobbies=('art', 'music', 'FRIEND', 'sport', 'animal'))


@app.route('/logout')
def logout_func():
    session['username'] = ''
    return render_template('index.html')


@app.route('/catalog')
def catalog_func():
    if 'product' in request.args:
        product = request.args['product']
        size = request.args['size']
        return render_template('catalog.html', p_name=product, p_size=size)
    return render_template('catalog.html')


@app.route('/users')
def users_func():
    return render_template('users.html')


@app.route('/assignment9', methods=['GET', 'POST'])
def ass9_func():
    user = ''
    username = ''
    if request.method == 'GET':
        if 'user' in request.args:
            user = request.args['user']
        return render_template('assignment9.html', p_user=user, dic_users=users, username=username,
                               request_method=request.method)
    elif request.method == 'POST':
        if 'logOutButton' in request.form:
            session['username'] = ''
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            # db
            found = True
            if found:
                session['username'] = username
                return render_template('assignment9.html', username=username)
    return render_template('assignment9.html')


## assignment10
from pages.assignment10.assignment10 import assignment10

app.register_blueprint(assignment10)

def get_user(user_id):
    res = requests.get(f'https://reqres.in/api/users/{user_id}')
    res = res.json()
    print(res)

    return res

@app.route('/assignment11/outer_source')
def assignment11Outersource():
    user_id = 0
    if "user_id" in request.args:
        user_id = int(request.args['user_id'])
    user = get_user(user_id)
    return render_template('assignment11_outersource.html', user=user)

def get_pockemons(num):
    pokemons = []
    for i in range(num):
        random_n = random.randint(1, 100)
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_n}')
        # res = requests.get('https://pokeapi.co/api/v2/pokemon/%s' % random_n)
        res = res.json()
        pokemons.append(res)
    return pokemons


@app.route('/req_backend')
def req_backend_func():
    num = 3
    if "number" in request.args:
        num = int(request.args['number'])
    pockemons = get_pockemons(num)
    return render_template('req_backend.html', pockemons=pockemons)


async def fetch_url(client_session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    # response = await session.get(url)
    async with client_session.get(url, ssl=False) as resp:
        response = await resp.json()
        return response


async def get_all_urls(num):
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        tasks = []
        for i in range(num):
            random_n = random.randint(1, 100)
            url = f'https://pokeapi.co/api/v2/pokemon/{random_n}'
            task = asyncio.create_task(fetch_url(client_session, url))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data


def get_pockemons_async(num=3):
    pockemons = asyncio.run(get_all_urls(num))
    return pockemons


@app.route('/req_backend_async')
def req_backend_async_func():
    num = 3
    if "number" in request.args:
        num = int(request.args['number'])
    pockemons = get_pockemons_async(num)
    return render_template('req_backend.html', pockemons=pockemons)


@app.route('/db_users', defaults={'user_id': -1, 'order': 'my order'})
@app.route('/db_users/<int:user_id>/<order>')
def get_users_func(user_id, order):
    query = 'select * from users where id=%s;' % user_id
    users = interact_db(query=query, query_type='fetch')
    if len(users) == 0:
        return_dict = {
            'status': 'failed',
            'message': 'user not found'
        }
    else:
        return_dict = {
            'status': 'success',
            f'id': users[0].id,
            'name': users[0].name,
            'email': users[0].email,
            'orders': order
        }
    return jsonify(return_dict)


@app.route('/assignment11/users')
def assignment11_func():
    return_dict = {}
    query = 'select * from users';
    users = interact_db(query=query, query_type='fetch')
    for user in users:
        return_dict[f'usr_{user.id}'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
