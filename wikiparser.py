#!/usr/bin/env python

import httplib2
import re
import BeautifulSoup

class WikiParser:
    def __init__(self,hyperlink):
        self.http = httplib2.Http() #initialize http2 library
        self.data = str(self.http.request(hyperlink)) #get html data from page
        
    def setLink(self,link): 
        self.data = str(self.http.request(link)) #get html data from page
        
    def getRelatedActs(self):
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData) #refill soup
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData) 
        relatedBandsList = list() #init return list
        for i in soup.contents:
            value = str(i) #buffer store
            if (not value.strip() ==",") and (not value.strip() =="]") and (not value.strip() =="[") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(value) #new bowl of soup
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                if "associated acts" in str(output).lower(): 
                    tdData = str(soup2.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData) #another bowl of soup with all td
                    aData = str(soup3.findAll("a")) #get all links in cell
                    relatedBands  = re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip text
                    relatedBandLinks  = re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(aData)) #strip link
                    for bandLinks in relatedBandLinks: #iterate and build dictionary
                        bandLinksIndex = relatedBandLinks.index(bandLinks)
                        relatedBandLinks[bandLinksIndex] = "http://en.wikipedia.org" + bandLinks
                        #relatedBandsDictionary[relatedBands[bandLinksIndex]] = relatedBandLinks[bandLinksIndex] #push into dictionary
                        relatedBandsDictionary = dict() #init dictionary
                        relatedBandsDictionary["band"] = relatedBands[bandLinksIndex]
                        relatedBandsDictionary["link"] = relatedBandLinks[bandLinksIndex]
                        relatedBandsList.append(relatedBandsDictionary)
                    return relatedBandsList
        return relatedBandsList #return blank
    
    def getBandMembers(self, Btype="current"):
        if(Btype.lower() =="former"): Btype = "['former&#160;members']"
        else: Btype = "['members']"            
        soup = BeautifulSoup.BeautifulSoup(self.data) #fill soup
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        
        relatedBandsList = list() #init return list
        i = iter(soup.contents)
        while True:
            try: value = i.next()
            except : break #exit if reached end of list
            strippedValue = str(value).strip()
            if (not strippedValue  ==",") and (not strippedValue  =="]") and (not strippedValue  =="[") and (not strippedValue  =="") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(strippedValue) #refill soup              
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                if Btype == str(output).lower():
                    nextRow= i.next()
                    nextRow= i.next()
                    soupPlus1 = BeautifulSoup.BeautifulSoup(str(nextRow))
                    tdData = str(soupPlus1.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData) 
                    tdData = tdData.replace("<td style=\"text-align:center;\" colspan=\"2\">","") # some cleaning
                    tdData = tdData.replace("</td>","")
                    tdData = tdData.split('<br />\\n')
                    for members in tdData:
                        relatedBands  = str(re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip text
                        relatedBandLinks  = str(re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip link
                        if(str(relatedBands).strip()=="[]"): #for members with no hyperlinks
                            relatedBands = str(members) 
                            relatedBandLinks = ""
                        else:
                            relatedBandLinks = "http://en.wikipedia.org" + relatedBandLinks
                            
                        relatedBands = self.stripArraytags(relatedBands)
                        relatedBandLinks= self.stripArraytags(relatedBandLinks)
                        #BandMembersDictionary[relatedBands] = relatedBandLinks
                        BandMembersDictionary = dict() #init dictionary
                        BandMembersDictionary["artist"] = relatedBands
                        BandMembersDictionary["link"] = relatedBandLinks
                        relatedBandsList.append(BandMembersDictionary)
                    return relatedBandsList
        return relatedBandsList #return blank
    
    def remove_html_tags(self,data):
        #http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
        p = re.compile(r'<.*?>')
        return p.sub('', data)
        
    def stripArraytags(self, data):
        data = str(data)
        data  = data.replace("\"","") #cleaning
        data  = data.replace("'","")
        data  = data.replace("[","")
        data  = data.replace("]","")
        data = data.strip()
        return data
        
    def getInstruments(self):
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData) #refill soup
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData) 
        relatedBandsDictionary = [] #init return list
        for i in soup.contents:
            value = str(i) #buffer store
            if (not value.strip() ==",") and (not value.strip() =="]") and (not value.strip() =="[") : #if data we are looking for
                soup2 = BeautifulSoup.BeautifulSoup(value) #new bowl of soup
                thData = str(soup2.findAll("th")) #find all header cells
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) #get text in header cell
                if "instruments" in str(output).lower(): 
                    tdData = str(soup2.findAll("td")) #get all cells
                    tdData = self.remove_html_tags( str(tdData))
                    tdData = self.stripArraytags(tdData)
                    relatedBandsDictionary = tdData.split(',')
                    return relatedBandsDictionary
        return relatedBandsDictionary #return blank
    
    def getName(self, type="band"):
        if(type.lower() == "artist"): type = "fn"
        else: type = "fn org"
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        headerText =  str(soup.findAll("span", { "class" : type })) #find title
        if(type=="fn"): relatedBandLinks  = re.compile('<span class="fn">(.*?)</span>', re.DOTALL | re.IGNORECASE).findall(str(headerText)) #clean it up
        else: relatedBandLinks  = re.compile('<span class="fn org">(.*?)</span>', re.DOTALL | re.IGNORECASE).findall(str(headerText)) #clean it up
        returnText =""
        try: returnText  = str(relatedBandLinks[0])
        except: return "" #return blank, if not found
        return returnText

if __name__ == '__main__':
    print "\n\n\n=================================================\n"
    #a = WikiParser("http://en.wikipedia.org/wiki/Soundgarden")
    #a = WikiParser("http://en.wikipedia.org/wiki/Chris_Cornell")
    a = WikiParser("http://en.wikipedia.org/wiki/Green_Jelly")
    #a = WikiParser("http://en.wikipedia.org/wiki/Radioactive_Chickenheads")
    print "\nName: "
    print a.getName("band")
    print "\nInstruments: "    
    print a.getInstruments()
    print "\nRelated Bands: "
    print a.getRelatedActs()
    print "\nCurrent Band Members: "
    print a.getBandMembers()
    print "\nFormer Band Members: "
    print a.getBandMembers("former")
    print "\n-----------------------------------------------------\n"    
    a.setLink("http://en.wikipedia.org/wiki/Chris_Cornell")
    print "\nName: "
    print a.getName("artist")
    print "\nInstruments: "    
    print a.getInstruments()
    print "\nRelated Bands: "
    print a.getRelatedActs()
    print "\nCurrent Band Members: "
    print a.getBandMembers()
    print "\nFormer Band Members: "
    print a.getBandMembers("former")
 