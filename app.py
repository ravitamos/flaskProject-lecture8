from flask import Flask, redirect, url_for
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home_func():  # put application's code here
    #db
    found= False
    if found:
        return render_template('index.html',name='ravit')
    else:
        return render_template('index.html')

@app.route('/assignment8')
def about_func():
    #db
    return render_template('assignment8.html', profile={'name': 'ravit', 'second': 'amos'},
                           university='bgu', fav_movies=['Lion king','the Avengers','AVATAR'], hobbies=('art', 'music','FRIEND','sport','animal'))


if __name__ == '__main__':
    app.run(debug=True)
