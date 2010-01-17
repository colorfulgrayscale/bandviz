#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""

import BeautifulSoup
import httplib2
import re

#messy wikipedia parser
class WikiParser: 
    def __init__(self,hyperlink):
        self.http = httplib2.Http() #initialize http2 library
        self.data = str(self.http.request(hyperlink)) #get html data from page
        
    def setLink(self,link): 
        self.data = str(self.http.request(link)) #get html data from page
        
    def getRelatedActs(self): #get list of related acts
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
                        bandLinks = str(bandLinks).replace("\"","").strip()
                        relatedBandLinks[bandLinksIndex] = "http://en.wikipedia.org" + bandLinks #prepend full url
                        relatedBandsDictionary = dict() #init dictionary
                        relatedBandsDictionary["band"] = self.remove_html_tags(self.remove_brackets(relatedBands[bandLinksIndex]))
                        relatedBandsDictionary["link"] = relatedBandLinks[bandLinksIndex]
                        relatedBandsList.append(relatedBandsDictionary)
                    return relatedBandsList #return list of all related acts and links
        return relatedBandsList #return blank
    
    def getBandMembers(self, Btype="current"): #get list of band members
        if(Btype.lower() =="former"): Btype = "['former&#160;members']" #magic strings to look for
        else: Btype = "['members']"            
        soup = BeautifulSoup.BeautifulSoup(self.data) #fill soup
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        relatedBandsList = list() #init return list
        i = iter(soup.contents) #init iterator
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
                    nextRow= i.next()#skip one, to ignore junk value
                    soupPlus1 = BeautifulSoup.BeautifulSoup(str(nextRow))
                    tdData = str(soupPlus1.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData) 
                    tdData = tdData.replace("<td style=\"text-align:center;\" colspan=\"2\">","") # some cleaning
                    tdData = tdData.replace("</td>","") #more cleaning for special cases
                    tdData = tdData.split('<br />\\n') #split by br for non href-ed members
                    for members in tdData:
                        relatedBands  = str(re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip text
                        relatedBandLinks  = str(re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() #strip link
                        if(str(relatedBands).strip()=="[]"): #for members with no hyperlinks
                            relatedBands = str(members) 
                            relatedBandLinks = ""
                        else:
                            relatedBandLinks = "http://en.wikipedia.org" + relatedBandLinks #prepend full wikipedia address
                        relatedBands = self.stripArraytags(relatedBands)
                        relatedBandLinks= self.stripArraytags(relatedBandLinks)
                        BandMembersDictionary = dict() #init dictionary
                        BandMembersDictionary["artist"] = self.remove_html_tags(self.remove_brackets(relatedBands)) #more cleaning
                        BandMembersDictionary["link"] = relatedBandLinks
                        relatedBandsList.append(BandMembersDictionary)
                    return relatedBandsList #return list of bands
        return relatedBandsList #return blank
    
    def remove_html_tags(self,data):
        #http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def remove_brackets(self,data): #strip brackets
        p = re.compile(r'(.*?)')
        return p.sub('', data)
    
        
    def stripArraytags(self, data): #strip special characters from str(Array)
        data = str(data)
        data  = data.replace("\"","") #cleaning
        data  = data.replace("'","")
        data  = data.replace("[","")
        data  = data.replace("]","")
        data = data.strip()
        return data
        
    def getInstruments(self): #get list of instruments played by artist
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
                    relatedBandsDictionary = tdData.split(',') #convert into list
                    return relatedBandsDictionary #return list with instruments
        return relatedBandsDictionary #return blank
    
    def getName(self): #get name of artist/band
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        headerText =  str(soup.findAll("title")) #find title text
        headerText = headerText.replace("(band)","") #strip verbage
        headerText = self.remove_brackets(headerText) 
        headerText = self.remove_html_tags(headerText)
        headerText  = self.stripArraytags(headerText)
        headerText = headerText.replace("- Wikipedia, the free encyclopedia","") #remove branding
        headerText  = headerText.strip() #remove spaces
        return headerText                        

if __name__ == '__main__':
    print "\n\n\n=================================================\n"
    #a = WikiParser("http://en.wikipedia.org/wiki/Soundgarden")
    #a = WikiParser("http://en.wikipedia.org/wiki/Chris_Cornell")
    #a = WikiParser("http://en.wikipedia.org/wiki/Green_Jelly")
    a = WikiParser("http://en.wikipedia.org/wiki/Tool_(band)")
    #a = WikiParser("http://en.wikipedia.org/wiki/Radioactive_Chickenheads")
    print "\nName: "
    print a.getName()
    print "\nInstruments: "    
    print a.getInstruments()
    print "\nRelated Bands: "
    print a.getRelatedActs()
    print "\nCurrent Band Members: "
    print a.getBandMembers()
    print "\nFormer Band Members: "
    print a.getBandMembers("former")
    print "\n-----------------------------------------------------\n"    
    a.setLink("http://en.wikipedia.org/wiki/Brad_Wilk")
    print "\nName: "
    print a.getName()
    print "\nInstruments: "    
    print a.getInstruments()
    print "\nRelated Bands: "
    print a.getRelatedActs()
    print "\nCurrent Band Members: "
    print a.getBandMembers()
    print "\nFormer Band Members: "
    print a.getBandMembers("former")
 