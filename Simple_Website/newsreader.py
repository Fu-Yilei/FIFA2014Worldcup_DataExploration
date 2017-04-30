# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:40:05 2017

@author: Frank Fu
"""
from urllib import *
from bs4 import BeautifulSoup
def read_news():
    html = urllib.request.urlopen("http://www.espnfc.com/index").read()
    soup = BeautifulSoup(html, "lxml")
    all_news = (soup.findChildren('h2'))
    return all_news