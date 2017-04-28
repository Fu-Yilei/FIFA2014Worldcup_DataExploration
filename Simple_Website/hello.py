# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:59:55 2017

@author: Frank Fu
"""

from flask import Flask, url_for
from flask import render_template

app = Flask(__name__)
import sqlite3 as lite
import sys

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

# @app.route('/questions/<int:question_id>'):    #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
@app.route('/teams/')
@app.route('/teams/<name>')
def team(name=None):
	"""
	con = lite.connect("fifa2014.db")
	cur = con.cursor()
	cur.execute("select id, title, author from books")
	rows = cur.fetchall()
 	
	return render_template("index.html", **locals())
	"""
	return render_template('teams.html', name=name)

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