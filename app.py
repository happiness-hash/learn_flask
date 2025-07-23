from flask import Flask,render_template
from markupsafe import escape
from flask import url_for
app = Flask(__name__)
name = 'Grey Li'
movies = [
    {'title':'My Neighbor Totoro','year':'1998'},
    {'title':"A Perfect World",'year':'1993'}

]

# @app.route('/')
# def hello():
#     return '<h1>Hello Totoro!</h1><img src  "http://helloflask.com/totoro.gif">'
@app.route('/')
def index():
    return render_template('index.html',name  = name ,movies = movies )
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route("/test")
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name = 'peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num = 2))
    return "Test page"