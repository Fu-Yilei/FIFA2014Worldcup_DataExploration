# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:27:51 2017

@author: Frank Fu
"""

import codecs
import csv
from bs4 import BeautifulSoup
data = []
soup = BeautifulSoup(open("2014 FIFA World Cup squads - Wikipedia.html",encoding = "utf-8"),"lxml")
#tables = soup.find('table', attrs = {'class':'sortable wikitable plainrowheaders jquery-tablesorter'})
count = 0
Whole_table = []
temp = []
all_tables = (soup.findChildren('table',attrs = {'class':'sortable wikitable plainrowheaders jquery-tablesorter'}))
for tables in all_tables:
    rows = tables.findChildren(['tr','th'])
    for row in rows:
        cells = row.findChildren(['td','th'])
        for cell in cells:
            
            if cell.string != 'No.' and cell.string !='Pos.' and cell.string != 'Player' and cell.string !='Date of birth (age)' and cell.string !='Caps' and cell.string !='Club':
                count = count+1
                temp.append(cell)
                if count == 6:
                    Whole_table.append(temp)
                    temp = []
                    count = 0

                
temp = []
RealData = []
for item in Whole_table:
    
    Number = item[0].string
    Name = item[2].find('a').string
    Position = item[1].find('a').string
    Birthday = item[3].find('span').find('span').string.split('-')
    Birthday_year = Birthday[0]
    Birthday_month = Birthday[1]
    Birthday_day = Birthday[2]
    Caps = item[4].string
    Club = item[5].find_all('a')[1].string
    
    temp.append(str(Number))
    temp.append(str(Position))
    temp.append(str(Name))
    temp.append(str(Birthday_year))
    temp.append(str(Birthday_month))
    temp.append(str(Birthday_day))
    temp.append(str(Caps))
    temp.append(str(Club))
    RealData.append(temp)
    temp = []
   # print (Name)

file = open("a.csv","w",encoding = "utf-8")
for items in RealData:
    for i in items:
        file.write(i + ",")
    file.write("\n")
file.close()
