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
    groupname = name
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from group_stage where Group_Name = \'"+str(groupname[-1])+"\'")
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
        cur.execute("select * from players inner join clubs on players.club_id = clubs.club_id where Name like \'%"+str(search)+"%\'")
        rows = cur.fetchall()                                                                                                                                                                                                                                                                                                                                                           
        return render_template('search.html',  **locals())
    
@app.route('/matches', methods = ["GET","POST"])
def matches(name=None):
    Cmnt =  []
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from matches")
    rows = cur.fetchall()
    
    curc = con.cursor()
    curc.execute("select * from comment")
    c = curc.fetchall()
    if request.method == "GET":
        return render_template('matches.html', **locals())
    else:
        comment = request.form["comment"]
        author = request.form["author"]
        matchid = request.form["matchid"]
        with con:
            cur = con.cursor()
            cur.execute("insert into comment (match_id, comment, author) values ('{}', '{}','{}')".format(matchid, comment, author))  
        return render_template('matches.html', **locals())
@app.route('/comments')
def comments(name=None):
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from comment inner join matches on comment.match_id = matches.match_id")
    rows = cur.fetchall()
    return render_template('comments.html', **locals())
@app.route('/matchdata/<name>')
def matchdata(name = None):
    con = lite.connect("fifa2014.db")
    cur = con.cursor()
    cur.execute("select * from lineups inner join players on lineups.Player_id = Players.id where lineups.match_id = "+name)
    rows = cur.fetchall()
    cur.execute("select * from goals inner join players on goals.Player_id = Players.id where goals.match_id = "+name)
    goals = cur.fetchall()
    cur.execute("select * from matches where match_id = "+name)
    matches = cur.fetchall()
    link = '/matchdata/'+str(name)
    return render_template('matchdata.html', **locals())

@app.route('/stats/<name>')
@app.route('/stats/<name>/<sort>')
def stat(name=None, sort=None):
    con = lite.connect("fifa2014.db")
    cur = con.cursor()

    if name == "referees":
        exstring = "select Name, Birthday_Year, Country_Name, Yellow_Cards, Yellow_To_Red_Cards, Red_Cards \
                        from referees r, countries c where c.Country_ID = r.Country"
    elif name == "players":
        exstring = "select p.Name, p.Pos, P.Jersey_No, c.Country_Name, cl.Club_Name, \
                                    g.goal_count, g.penalty_goals, g.own_goals, \
                                    d.total_yc, d.total_rc \
                    from players p, countries c, clubs cl \
                    inner join ( \
                                select Player_ID, count(*) as goal_count, \
                                sum(case when Special_Type = 'PENALTY' then 1 else 0 end) as penalty_goals, \
                                sum(case when Special_Type = 'OWN_GOAL' then 1 else 0 end) as own_goals \
                                from goals \
                                group by Player_ID \
                                ) as g \
                    on p.Id = g.Player_ID \
                    inner join ( \
                                select Player_ID, \
                                sum(case when Card = 'YC' then 1 else 0 end) as total_yc, \
                                sum(case when Card = 'RC' then 1 else 0 end) as total_rc \
                                from discipline \
                                group by Player_ID) as d \
                    on p.Id = d.Player_ID \
                    where p.Country_ID = c.Country_ID and p.Club_ID = cl.Club_ID"
    if not sort == None:
        exstring += " order by {} desc".format(sort)

    cur.execute( exstring )
    rows = cur.fetchall()
    return render_template('stats.html', **locals())
if __name__ == '__main__':
    app.run()