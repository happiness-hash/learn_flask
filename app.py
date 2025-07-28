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


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user = user)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html',movies = movies )


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html',user = user),404

# @app.route('/')
# def index():
#     user = User.query.first()
#     movies = Movie.query.all()
#     return render_template('index.html',user = user,movies = movies)


# @app.route('/')
# def index():
#     return render_template('index.html',name  = name ,movies = movies )
@app.route('/user/<name>')
def user_page(name):
    # return f'User: {escape(name)}'
    return render_template("index.html",user = {"name": name})


@app.route("/test")
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name = 'peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num = 2))
    return "Test page"