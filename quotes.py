from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pyscopg2://postgres:password@localhost/quotes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gnefliss:DCGdgI6ikn5APZuAJDVwz2IyHnQIeQyT@isilo.db.elephantsql.com/gnefliss'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Favquotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))
    date = db.Column(db.Date)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # color = ['magenta', 'green', 'yellow']
    # return render_template('index.html', quote1='', colors=color)
    result = Favquotes.query.all()
    return render_template('index.html', result=result)


@app.route('/about')
def about():
    return '<h1>About us</h1>'


@app.route('/quotes')
def quotes():
    return render_template('quotes.html')


@app.route('/process', methods=['POST'])
def processs():
    author = request.form['author']
    quote = request.form['quote']
    date = request.form['date']
    quotedata = Favquotes(author=author, quote=quote, date=date)
    db.session.add(quotedata)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = False
    app.run()
