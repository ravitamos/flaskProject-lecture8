from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = '123'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)



users = {'user1': {'name': 'yossi', 'email': 'yo@gmail.com'},
         'user2': {'name': 'ravit', 'email': 'ra@gmail.com'},         'user3': {'name': 'roi', 'email': 'ro@gmail.com'},
         'user4': {'name': 'lir', 'email': 'li@gmail.com'},
         'user5': {'name': 'shir', 'email': 'sh@gmail.com'}}
username=''
@app.route('/')
def home_func():  # put application's code here
    #db
    found= False
    if found:
        return render_template('index.html',name='ravit')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
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
    #db
    return render_template('assignment8.html', profile={'name': 'ravit', 'second': 'amos'},
                           university='bgu', fav_movies=['Lion king','the Avengers','AVATAR'], hobbies=('art', 'music','FRIEND','sport','animal'))

@app.route('/logout')
def logout_func():
    session['username'] = ''
    return render_template('index.html')

@app.route('/catalog')
def catalog_func():
    if 'product' in request.args:
        product = request.args['product']
        size = request.args['size']
        return render_template('catalog.html',p_name=product ,p_size=size)
    return render_template('catalog.html')

@app.route('/users')
def users_func():
    return render_template('users.html')

@app.route('/assignment9', methods=['GET','POST'])
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
            #db
            found = True
            if found:
                session['username'] = username
                return render_template('assignment9.html', username=username)
    return render_template('assignment9.html')

## assignment10
from pages.assignment10.assignment10 import assignment10
app.register_blueprint(assignment10)

if __name__ == '__main__':
    app.run(debug=True)

