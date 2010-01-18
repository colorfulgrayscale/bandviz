#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""


class Artist:
    """Artist class to store artist entity information"""    
    
    
    def __init__(self, name="",instrument=""):
        """Constructor"""
        #name of artist
        self.name = name
        #instruments played by artist
        self.instrument = instrument
        #list of all the bands to which the artist belongs
        self.bandList = []
        #list of all the bands to which the artist belonged
        self.formerBands = [] 
    
    def setName(self, name):
        """Setter for name of artist."""
        self.name = name
    
    def setInstrument(self, instrument):
        """Setter for instruments played by artist"""
        self.instrument = instrument
    
    def hasBand(self, arg_band):
        """Checks if the supplied band is one which the artist belongs to.
            Return a boolean."""
        if(isinstance(arg_band, Band)):
            return arg_band in self.bandList
    
    def addBand(self, arg_band):
        """Links supplied band with artist."""
        if(isinstance(arg_band, Band)):
            self.bandList.append(arg_band)

    def addFormerBand(self, arg_band):
        """Links supplied band with artist as a 'former band'."""
        if(isinstance(arg_band, Band)):
            self.formerBands.append(arg_band)
    
    def __str__(self):
        """toString method, Returns string"""
        returnString = (self.name + " is a " + self.instrument + " and is in "
                         + str(len(self.bandList)) + " band(s) {")
        for i in self.bandList:
            returnString += str(i.name) + ", "
        return returnString + "}";
    
    def __eq__(self, other):
        """Compares two artists, returns boolean."""
        if isinstance(other, Artist):
            return self.name.lower() == other.name.lower()
        return NotImplemented
    
    def __ne__(self, other):
        """Compares two artists, returns boolean."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result    


class Band:
    """Band class to store band entity information"""    
    
    
    def __init__(self, name=""):
        """Constructor"""
        #Store name of band
        self.name = name
        #Store list of artists in band
        self.artistList = list()
        #Store list of artists who used to be in the band
        self.formerArtistList = list() 
        
    def setName(self, name):
        """Setter for band name"""
        self.name = name
    
    def hasArtist(self, arg_artist):
        """Checks if an artist is a part of this band. Returns Boolean"""
        if(isinstance(arg_artist, Artist)):
            return arg_artist in self.artistList
    
    def hasFormerArtist(self, arg_artist):
        """Checks if an artist was a part of ths band. Returns Boolean"""
        if(isinstance(arg_artist, Artist)):
            return arg_artist in self.formerArtistList


    def addArtist(self, arg_artist):
        """Link an artist with this band"""
        if(isinstance(arg_artist, Artist)):
            self.artistList.append(arg_artist)

    def addFormerArtist(self, arg_artist):
        """Link a former band member with this band"""
        if(isinstance(arg_artist, Artist)):
            self.formerArtistList.append(arg_artist)
    
    def __str__(self):
        """toString. Returns String"""
        returnString = (self.name + " has " + str(len(self.artistList)) +
                        " member(s)")
        for i in self.artistList:
            returnString +=  "\n\t -> "+str(i)
        returnString += "\n\tFormer member(s)"    
        for i in self.formerArtistList:
            returnString +=  "\n\t -> " + str(i) 
            
        return returnString
    
    def getArtistArray(self):
        """Getter method for list of artists."""
        return self.artistList
    
    def __eq__(self, other):
        """Compare two bands. Returns boolean."""
        if isinstance(other, Band):
            return self.name.lower() == other.name.lower()
        return NotImplemented
    
    def __ne__(self, other):
        """Compare two bands. Returns boolean."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result    


class BandManager:
    """Manages linking bands and artists"""


    def __init__(self, name=""):
        """Constructor"""
        self.artistList = list() #maintain list of artists
        self.BandList = list()  #maintain list of bands
        #graphViz default graph attributes
        self.vizBandBackgroundColor = "black"
        self.vizBandFontColor = "white"
        self.vizBandShape = "egg"
        self.vizArtistBackgroundColor = "gray"
        self.vizArtistFontColor = "black"
        self.vizArtistShape = "ellipse"
        self.vizBackground = "white"
        self.vizArrowColor = "blue4"
        self.vizOutpuFileName = "bandviz.gv"
        
    def addArtist(self, arg_artist, instrument=""):
        """Add artist to be managed by BandManager"""
        if(isinstance(arg_artist,Artist)):    #make sure it's an artist
            if arg_artist in self.artistList: #if artist already exists in list
                    artistIndex = self.artistList.index(arg_artist)
                    if not str(arg_artist.instrument).strip() == "":
                        self.artistList[artistIndex].instrument = (
                            arg_artist.instrument) #update instruments if needed
            else:
                self.artistList.append(arg_artist) #add artist to bandmanager
        else:
            #if called with string, make a new artist and recall this function
            if(isinstance(arg_artist,str)): 
                self.addArtist(Artist(arg_artist,instrument))

    def bandExists(self, bandString):
        """Checks if band is already being managed. Returns Boolean"""
        bandVar = Band(bandString)
        return bandVar in self.BandList

    def artistExists(self, artistString):
        """Checks if artist is already being managed. Returns Boolean"""
        artistVar = Artist(artistString)
        return artistVar in self.artistList
    
    def addBand(self, arg_band):
        """Adds band to be managed by BandManager"""
        if(isinstance(arg_band,Band)): #make sure the argument is a band
            if not arg_band in self.BandList: #if not already managed
                self.BandList.append(arg_band) #add band to band manager
        else:
            #if band DNE, create a Band object and recall
            if(isinstance(arg_band,str)): 
                self.addBand(Band(arg_band))

    def link(self,artist, band,former=False):
        """Links together an artist with a band."""
        if(isinstance(band,Band)):
            if(isinstance(artist,Artist)): #make sure they are right datatypes
                #link band with artist
                if artist in self.artistList:
                    artistIndex = self.artistList.index(artist)
                    #not already linked
                    if not self.artistList[artistIndex].hasBand(band): 
                        if former: #if the band & member are not together
                            self.artistList[artistIndex].addFormerBand(band)
                        else:    
                            self.artistList[artistIndex].addBand(band) #link
                else: 
                    #band not found. Create artist and recall function
                    self.addArtist(artist);
                    self.link(artist,band,former);
                    return;
                #link artist with band
                if band in self.BandList:
                    bandIndex = self.BandList.index(band)
                    #check if not already linked
                    if not self.BandList[bandIndex].hasArtist(artist): 
                        if former: #if the band and member are not together
                            self.BandList[bandIndex].addFormerArtist(artist) 
                        else:
                            self.BandList[bandIndex].addArtist(artist) #link
                else:
                    #create band and recall
                    self.addBand(band);
                    self.link(artist,band,former);
            else:
                print "\t\t[-] Wrong datatype sent to linker!"
        else:
            print "\t\t[-] Wrong datatype sent to linker!"

    def printAllArtists(self):
        """Prints all artists managed by BandManager"""
        returnString =""
        for i in self.artistList:
            returnString +=  str(i) + "\n"
        return returnString   

    def printAllBands(self):
        """Prints all bands managed by BandManager"""
        returnString =""
        for i in self.BandList:
            returnString +=  str(i) + "\n"
        return returnString

    def generateGV(self, former=False):
        """Generates Graphviz file"""
        printString = "" #stores data to be written to file
        #header information
        vizHeader = ("/* generated by bandViz\n"
                " * http://www.colorfulgrayscale.com/software/bandviz/\n *\n"
                " * To make a graph from this file, download GraphViz "
                "from\n * http://www.graphviz.org/ and point it to this "
                "file.\n */\n\n")
        vizHeader =  vizHeader + "digraph bandviz {"
        vizHeader = vizHeader + ("\n\n\t/* Global Formatting */\n")        
        vizHeader = vizHeader  + ("\n\tgraph [fontsize = \"20\", "
                    "label = \"generated with bandViz\", size = \"60\", "
                    "overlap=false, ratio = auto, bgcolor=\"" +
                    self.vizBackground + "\"];")
        vizHeader = vizHeader + ("\n\tnode [style=filled, "
                    "fontsize = \"16\", size=\"30\", overlap=false];\n")
        printString = vizHeader
        printString = printString + "\n\t/* Formatting for Band Nodes */\n"
        #band formatting information
        for bandsIter in self.BandList:
                if bandsIter.artistList or former:
                    bandString = ("\n\t\"" + bandsIter.name + "\" " +
                        "[shape=\""+self.vizBandShape+"\", style=\"filled\", "
                        "color=\""+self.vizBandBackgroundColor+"\", "
                        "fontcolor=\""+ self.vizBandFontColor+ "\"];")
                    printString = printString + bandString
        printString = printString+ "\n\n\t/* Formatting for Artist Nodes */\n"
        #artist formatting information
        for artistsIter in self.artistList:
            if artistsIter.bandList:
                artistString = ("\n\t\"" + artistsIter.name + "\" " +
                    "[shape=\"" + self.vizArtistShape+"\", style=\"filled\", "
                    "color=\"" + self.vizArtistBackgroundColor+"\", "
                    "fontcolor=\"" + self.vizArtistFontColor + "\"];")
                printString = printString + artistString
            if former and artistsIter.formerBands and not artistsIter.bandList:
                artistString = ("\n\t\"" + artistsIter.name + "\" " +
                    "[shape=\"" + self.vizArtistShape + "\", style=\"filled\", "
                    "color=\"" + self.vizArtistBackgroundColor + "\", "
                    "fontcolor=\"" + self.vizArtistFontColor + "\"];")
                printString = printString + artistString
        printString = printString + "\n\n\t/* Node Connections*/\n"
        #note linkages
        for bandIterator in self.BandList:
            for artistIterator in bandIterator.artistList:
                printString = (printString + "\n\t\"" +  artistIterator.name +
                    "\"" +  " -> " + "\"" + bandIterator.name  + "\"" +
                    " [color=\"" + self.vizArrowColor + "\"];")
        for bandIterator in self.BandList:
            for artistIterator in bandIterator.formerArtistList:
                printString = (printString + "\n\t\"" + artistIterator.name +
                    "\"" + " -> " + "\"" +  bandIterator.name  + "\"" +
                    " [arrowhead=onormal, color=\"" + self.vizArrowColor +
                    "\"];")
        printString = printString + "\n}"
        #open file and write contents
        filename = self.vizOutpuFileName
        file = open(filename, 'w')
        file.write(printString)
        file.close()
