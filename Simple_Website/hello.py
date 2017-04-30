# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:59:55 2017

@author: Frank Fu
"""

from flask import Flask, url_for
from flask import render_template
from urllib import *
from bs4 import BeautifulSoup



app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/teams')
def team(name=None):
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