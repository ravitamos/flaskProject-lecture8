from flask import Blueprint, render_template
from interact_with_db import interact_db
from flask import Flask, redirect, url_for
from flask import request

# assignment10 blueprint definition
assignment10 = Blueprint('assignment10', __name__, static_folder='static', static_url_path='/assignment10', template_folder='templates')


# Routes
@assignment10.route('/assignment10')
def index():
    query = 'select * from users;'
    users = interact_db(query=query, query_type='fetch')
    return render_template('assignment10.html', users=users)

@assignment10.route('/Insert_user', methods=['POST'])
def func_insert():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    query = "INSERT INTO users(name, email, password) values ('%s','%s','%s');" % (name, email, password)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment10')

# Routes
@assignment10.route('/Update_users',methods=['POST'])
def func_up():
    user_id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    query = "UPDATE users SET name='%s',email='%s' WHERE id='%s';" % (name, email, user_id)
    interact_db(query=query, query_type='commit')
    return render_template('assignment10.html')


@assignment10.route('/Delete_user', methods=['POST'])
def func_del():
    user_id = request.form['id']
    query = "DELETE FROM  users WHERE id='%s';" % user_id
    interact_db(query=query, query_type='commit')
    return redirect('/assignment10')

# Routes



