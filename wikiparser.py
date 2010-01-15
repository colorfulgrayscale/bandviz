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
    def getRelatedActs(self):
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
    
    def getBandMembers(self, Btype="current"):
        if(Btype.lower() =="former"):
            Btype = "['former&#160;members']"
        else:
            Btype = "['members']"            
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        relatedBands = "" 
        BandMembersDictionary = {'':''} #init return dictionary
        i = iter(soup.contents)
        while True:
            try: value = i.next()
            except : break
            strippedValue = str(value).strip()
            if (not strippedValue  ==",") and (not strippedValue  =="]") and (not strippedValue  =="[") and (not strippedValue  =="") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(strippedValue)               
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                if Btype == str(output).lower():
                    nextRow= i.next()
                    nextRow= i.next()
                    soupPlus1 = BeautifulSoup.BeautifulSoup(str(nextRow))
                    tdData = str(soupPlus1.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData)
                    tdData = tdData.replace("<td style=\"text-align:center;\" colspan=\"2\">","")
                    tdData = tdData.replace("</td>","")
                    tdData = tdData.split('<br />\\n')
                    for members in tdData:
                        relatedBands  = str(re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip text
                        relatedBandLinks  = str(re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip link
                        if(str(relatedBands).strip()=="[]"):
                            relatedBands = str(members)
                            relatedBandLinks = ""
                        else:
                            relatedBandLinks = "http://en.wikipedia.org" + relatedBandLinks
                        relatedBands = relatedBands.replace("\"","")
                        relatedBands = relatedBands.replace("'","")
                        relatedBands = relatedBands.replace("[","")
                        relatedBands = relatedBands.replace("]","")
                        relatedBandLinks= relatedBandLinks.replace("\"","")
                        relatedBandLinks= relatedBandLinks.replace("'","")
                        relatedBandLinks = relatedBandLinks.replace("[","")
                        relatedBandLinks= relatedBandLinks.replace("]","")
                        BandMembersDictionary[relatedBands] = relatedBandLinks
                    return BandMembersDictionary
        return BandMembersDictionary
    
a = WikiParser("http://en.wikipedia.org/wiki/Soundgarden")
#a = WikiParser("http://en.wikipedia.org/wiki/Radioactive_Chickenheads")

print "\nrelated bands\n"
print a.getRelatedActs()
print "\ncurrent band members\n"
print a.getBandMembers()
print "\nformer band members\n"
print a.getBandMembers("former")

