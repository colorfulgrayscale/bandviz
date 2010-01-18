#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""


import re
import BeautifulSoup
import httplib2


class WikiParser:
    """A messy wikipedia parser"""
    
    def __init__(self,hyperlink="http://en.wikipedia.org/wiki/Tool_(band)"):
        """constructor"""
        self.http = httplib2.Http() #initialize http2 library
        self.data = str(self.http.request(hyperlink)) #get html data from page
        
    def setLink(self,link="http://en.wikipedia.org/wiki/Tool_(band)"):
        """Make the wikiparser point to a different page"""
        self.data = str(self.http.request(link)) #get html data from page
        
    def getRelatedActs(self): 
        """Returns a list of associated acts"""
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        tableData =  str(soup.findAll("table",
                                { "class" : "infobox vcard" })) #find info box
        soup = BeautifulSoup.BeautifulSoup(tableData) #refill soup
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData) 
        relatedBandsList = list() #init return list
        for i in soup.contents:
            value = str(i) #buffer store
            #if data we are looking for
            if ((not value.strip() ==",") and (not value.strip() =="]") and
                (not value.strip() =="[")) : 
                soup2 = BeautifulSoup.BeautifulSoup(value) #new bowl of soup
                thData = str(soup2.findAll("th")) #find all header cells
                #get text in header cell
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) 
                if "associated acts" in str(output).lower(): 
                    tdData = str(soup2.findAll("td")) #get all cells
                    #another bowl of soup with all td
                    soup3 = BeautifulSoup.BeautifulSoup(tdData) 
                    aData = str(soup3.findAll("a")) #get all links in cell
                    #strip text
                    relatedBands  = re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(aData))
                    #strip link
                    relatedBandLinks  = re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(aData)) 
                     #iterate and build dictionary
                    for bandLinks in relatedBandLinks:
                        bandLinksIndex = relatedBandLinks.index(bandLinks)
                        bandLinks = str(bandLinks).replace("\"","").strip()
                        #prepend full url
                        relatedBandLinks[bandLinksIndex] = ("http://en.wikipedia.org"
                                                            + bandLinks )
                        relatedBandsDictionary = dict() #init dictionary
                        relatedBandsDictionary["band"] = self.remove_html_tags(self.remove_brackets(relatedBands[bandLinksIndex]))
                        relatedBandsDictionary["link"] = relatedBandLinks[bandLinksIndex]
                        relatedBandsList.append(relatedBandsDictionary)
                    #return list of all related acts and links
                    return relatedBandsList 
        #return blank
        return relatedBandsList 
    
    def getBandMembers(self, Btype="current"):
        """Returns a list of band members. Argument decides weather to get
            current members or former members."""
        #magic strings to look for
        if(Btype.lower() =="former"): Btype = "['former&#160;members']" 
        else: Btype = "['members']"            
        soup = BeautifulSoup.BeautifulSoup(self.data) #fill soup
        #find info box
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) 
        soup = BeautifulSoup.BeautifulSoup(tableData)
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData)
        relatedBandsList = list() #init return list
        i = iter(soup.contents) #init iterator
        while True:
            try: value = i.next()
            except : break #exit if reached end of list
            strippedValue = str(value).strip()
            #if data we are looking for
            if ((not strippedValue  ==",") and (not strippedValue  =="]") and
                (not strippedValue  =="[") and (not strippedValue  =="")) : 
                soup2 = BeautifulSoup.BeautifulSoup(strippedValue) #refill soup              
                thData = str(soup2.findAll("th")) #find all header cells
                #get text in header cell
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) 
                if Btype == str(output).lower():
                    nextRow= i.next()
                    nextRow= i.next()#skip one, to ignore junk value
                    soupPlus1 = BeautifulSoup.BeautifulSoup(str(nextRow))
                    tdData = str(soupPlus1.findAll("td")) #get all cells
                    soup3 = BeautifulSoup.BeautifulSoup(tdData)
                     # some cleaning
                    tdData = tdData.replace("<td style=\"text-align:center;\" colspan=\"2\">","")
                    #more cleaning for special cases
                    tdData = tdData.replace("</td>","") 
                    #split by br for non href-ed members
                    tdData = tdData.split('<br />\\n') 
                    for members in tdData:
                        #strip text
                        relatedBands  = str(re.compile('\">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(str(members))).strip()
                        #strip link
                        relatedBandLinks  = str(re.compile('href=\"(.*?)title', re.DOTALL | re.IGNORECASE).findall(str(members))).strip() 
                        #for members with no hyperlinks
                        if(str(relatedBands).strip()=="[]"): 
                            relatedBands = str(members) 
                            relatedBandLinks = ""
                        else:
                            #prepend full wikipedia address
                            relatedBandLinks = ("http://en.wikipedia.org" +
                                                relatedBandLinks )
                        relatedBands = self.stripArraytags(relatedBands)
                        relatedBandLinks= self.stripArraytags(relatedBandLinks)
                        BandMembersDictionary = dict() #init dictionary
                        #more cleaning
                        BandMembersDictionary["artist"] = self.remove_html_tags(self.remove_brackets(relatedBands)) 
                        BandMembersDictionary["link"] = relatedBandLinks
                        if (not "list of" in str(BandMembersDictionary["artist"]).lower()
                            and not "see below" in str(BandMembersDictionary["artist"]).lower()
                            and not "contributors" in str(BandMembersDictionary["artist"]).lower()):
                            relatedBandsList.append(BandMembersDictionary)
                    return relatedBandsList #return list of bands
        return relatedBandsList #return blank
    
    def remove_html_tags(self,data):
        """Strip html tags from text. Returns String."""
        #http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def remove_brackets(self,data):
        """Strip bracket tags from text. Returns String."""
        p = re.compile(r'(.*?)')
        return p.sub('', data)
    
        
    def stripArraytags(self, data):
        """strip special characters from str(Array). Returns String."""
        data = str(data)
        data  = data.replace("\"","") 
        data  = data.replace("'","")
        data  = data.replace("[","")
        data  = data.replace("]","")
        data = data.strip()
        return data
    
    def extractANSIfromUTF(self, utfText):
        """Extract ANSI. Does not work yet"""
        utfText = utfText.replace("\\\\","\\")
        utfText = utfText.decode('latin-1')
        return utfText        
        
    def getInstruments(self):
        """Returns a list of instruments which the artist plays"""
        soup = BeautifulSoup.BeautifulSoup(self.data)
        #find info box
        tableData =  str(soup.findAll("table", { "class" : "infobox vcard" })) 
        soup = BeautifulSoup.BeautifulSoup(tableData) #refill soup
        rowData = str(soup.findAll("tr")) #get all rows
        soup = BeautifulSoup.BeautifulSoup(rowData) 
        relatedBandsDictionary = [] #init return list
        for i in soup.contents:
            value = str(i) #buffer store
            #if data we are looking for
            if ((not value.strip() ==",") and (not value.strip() =="]") and
                (not value.strip() =="[") ): 
                soup2 = BeautifulSoup.BeautifulSoup(value) #new bowl of soup
                thData = str(soup2.findAll("th")) #find all header cells
                #get text in header cell
                output  = re.compile('>(.*?)</', re.DOTALL | re.IGNORECASE).findall(str(thData)) 
                if "instruments" in str(output).lower(): 
                    tdData = str(soup2.findAll("td")) #get all cells
                    tdData = self.remove_html_tags( str(tdData))
                    tdData = self.stripArraytags(tdData)
                    #convert into list
                    relatedBandsDictionary = tdData.split(',') 
                    #return list with instruments
                    return relatedBandsDictionary 
        return relatedBandsDictionary #return blank
    
    def getName(self):
        """Returns name of band/artist"""
        soup = BeautifulSoup.BeautifulSoup(self.data) 
        headerText =  str(soup.findAll("title")) #find title text
        #a lot of cleaning
        headerText = headerText.replace("(band)","") 
        headerText = headerText.replace("(musician)","") 
        headerText = self.remove_brackets(headerText) 
        headerText = self.remove_html_tags(headerText)
        headerText  = self.stripArraytags(headerText)
        #remove branding
        headerText = headerText.replace("- Wikipedia, the free encyclopedia","") 
        headerText  = headerText.strip() #remove spaces
        return headerText                        
