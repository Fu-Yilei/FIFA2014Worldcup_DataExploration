# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:59:55 2017

@author: Frank Fu
"""

from flask import Flask, render_template, redirect, url_for
import flask
import sqlite3 as lite
import sys
import urllib
from bs4 import BeautifulSoup
from flask.ext.sqlalchemy import SQLALchemy
from flask.ext.script import Manager
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:fuyilei@96@localhost:3306/fifa2014'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)

def read_news():
    html = urllib.request.urlopen("http://www.espnfc.com/index").read()
    soup = BeautifulSoup(html, "lxml")
    all_news = (soup.findChildren('h2'))
    f=open('./static/news.json','w')
    for i in range(5):
        f.write(str(all_news[i]))
    f.close()
    return all_news


@app.route('/')
def index(name=None):
    read_news()
    return render_template('index.html',  name = name)
# @app.route('/questions/<int:question_id>'):    #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
@app.route('/teams/')
@app.route('/teams/<name>')
def team(name=None):
    result = db.engine.execute("select * from clubs")
    return render_template('teams.html',  name=name)

@app.route('/tables')
def table(name=None):
    return render_template('tables.html', name=name)

@app.route('/matches')
def match(name=None):
    return render_template('matches.html', name=name)

@app.route('/stats')
def stat(name=None):
    return render_template('stats.html', name=name)
if __name__ == '__main__':
    app.run()