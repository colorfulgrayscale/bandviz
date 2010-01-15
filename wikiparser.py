#!/usr/bin/env python

import httplib2
from pyparsing import *
import re
import BeautifulSoup




#http = httplib.HTTP()

http = httplib2.Http()
data = str(http.request('http://en.wikipedia.org/wiki/Adam_Jones_%28musician%29'))

soup = BeautifulSoup.BeautifulSoup(data)
data = str(soup.prettify())

"""
filename = "output.html"
file = open(filename, 'w')
file.write(data)
file.close()
"""

#print data

tableData =  str(soup.findAll("table", { "class" : "infobox vcard" }))
soup = BeautifulSoup.BeautifulSoup(tableData)
data = str(soup.prettify())

rowData = str(soup.findAll("tr"))
soup = BeautifulSoup.BeautifulSoup(rowData)
#print rowData;
for i in soup.contents:
    value = str(i)
    if (not value.strip() ==",") and (not value.strip() =="]") and (not value.strip() =="[") :
        print  value + "\n-------------\n"
        
    
    
#for row in rowData:
 #   print "\n-----\n"+ str(row)



"""
greet = Word( alphas ) + "," + Word( alphas ) + "!"
greeting = greet.parseString( "Hello, World!" )
print greeting
"""


