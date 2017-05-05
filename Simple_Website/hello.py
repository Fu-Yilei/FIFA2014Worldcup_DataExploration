# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:59:55 2017

@author: Frank Fu
"""

from flask import Flask, render_template, redirect, url_for, request
import flask
import sqlite3 as lite
import sys
import urllib
from bs4 import BeautifulSoup


app = Flask(__name__)


def read_news():
    html = urllib.request.urlopen("http://www.espnfc.com/index").read()
    soup = BeautifulSoup(html, "lxml")
    all_news = (soup.findChildren('h2'))[0:5]
    f=open('./static/news.json','w')
    for i in range(5):
        f.write(str(all_news[i]))
    f.close()
    return all_news


@app.route('/')
def index(name=None):
    return render_template('index.html', **locals())
# @app.route('/questions/<int:question_id>'):    #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
@app.route('/groups/<name>')
def group(name=None):
    teamname = name
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from group_stage where Group_Name = \'"+str(name[-1])+"\'")
    rows = cur.fetchall()
    return render_template('groups.html', **locals())

@app.route('/search', methods = ["GET","POST"])
def search(name=None):
    if request.method == "GET":
        return render_template('search.html', name=name)
    else:
        search = request.form["search"]
        con = lite.connect("fifa2014.db")
        cur = con.cursor()
        cur.execute("select * from players where Name like \'%"+str(search)+"%\'")
        rows = cur.fetchall()                                                                                                                                                                                                                                                                                                                                                           
        return render_template('search.html',  **locals())

@app.route('/matches')
def match(name=None):
    return render_template('matches.html', name=name)

@app.route('/stats/<name>')
def stat(name=None):
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from \'"+str(name)+"\'")
    rows = cur.fetchall()
    return render_template('stats.html', **locals())

if __name__ == '__main__':
    app.run()