#!/usr/bin/env python

import httplib2
from pyparsing import *
import re
import BeautifulSoup


class WikiParser:
    def __init__(self,hyperlink):
        self.http = httplib2.Http() #initialize http2 library
        self.data = str(self.http.request(hyperlink)) #get html data from page
    def setLink(self,link): 
        self.data = str(self.http.request(hyperlink)) #get html data from page
    def getRelatedBands(self):
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        relatedBands = "" 
        relatedBandsDictionary = {'':''} #init return dictionary
        for i in soup.contents:
            value = str(i)
            if (not value.strip() ==",") and (not value.strip() =="]") and (not value.strip() =="[") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(value)
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                if "associated acts" in str(output).lower(): 
                    tdData = str(soup2.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData)
                    aData = str(soup3.findAll("a")) #get all links in cell
                    relatedBands  = re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip text
                    relatedBandLinks  = re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip link
                    for bandLinks in relatedBandLinks:
                        bandLinksIndex = relatedBandLinks.index(bandLinks)
                        relatedBandLinks[bandLinksIndex] = "http://en.wikipedia.org" + bandLinks
                        relatedBandsDictionary[relatedBands[bandLinksIndex]] = relatedBandLinks[bandLinksIndex] #push into dictionary
                    return relatedBandsDictionary
        return relatedBandsDictionary
    def getBandMembers(self):
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        relatedBands = "" 
        relatedBandsDictionary = {'':''} #init return dictionary
        for i in soup.contents:
            value = str(i)
            valueIndex = soup.contents.index(i)
            if (not value.strip() ==",") and (not value.strip() =="]") and (not value.strip() =="[") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(value)               
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                print str(output) + " ** " + str(soup2.contents) + ">>" + str(valueIndex) +  " >>\n---\n"
                if "['members']" == str(output).lower():
                    nextRow = str(soup.contents[valueIndex+1])
                    newIndex = valueIndex+1
                    print "!!MemberText:" + str(valueIndex) + "-" + str(++i) + "!!!\n\n"
                    soupPlus1 = BeautifulSoup.BeautifulSoup(nextRow)
                    #soup.contents[valueIndex+2].extract()
                    tdData = str(soupPlus1.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData)
                    print "^^^" + str(tdData)
                    aData = str(soup3.findAll("a")) #get all links in cell
                    relatedBands  = re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip text
                    relatedBandLinks  = re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip link
                    return
                
        return relatedBandsDictionary
                
        
a = WikiParser("http://en.wikipedia.org/wiki/Soundgarden")
a.getBandMembers()
#hyperlink = "http://en.wikipedia.org/wiki/Adam_Jones_(musician)"

#http = httplib.HTTP()



"""
filename = "output.html"
file = open(filename, 'w')
file.write(data)
file.close()
"""

#print data

        
    
    
#for row in rowData:
 #   print "\n-----\n"+ str(row)



"""
greet = Word( alphas ) + "," + Word( alphas ) + "!"
greeting = greet.parseString( "Hello, World!" )
print greeting
"""


