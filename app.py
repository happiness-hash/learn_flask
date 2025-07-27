from flask import Flask,render_template
from markupsafe import escape
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import click
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
db = SQLAlchemy(app)
name = 'Grey Li'
movies = [
    {'title':'My Neighbor Totoro','year':'1998'},
    {'title':"A Perfect World",'year':'1993'}

]
class User(db.Model):
    id = db.Column(db.Integer,primary_key  = True)
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
@click.option('--drop',is_flag = True,help = 'Create afterr drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title':"My Neighbor Totoro",'year' :'1988'},
        {'title':'Dead Poets Society','year':'1989'}
]
    user = User(name = name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title = m['title'],year = m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user = user,movies = movies)


# @app.route('/')
# def index():
#     return render_template('index.html',name  = name ,movies = movies )
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