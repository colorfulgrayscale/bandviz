#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""

#artist entity
class Artist:
    def __init__(self, name="",instrument=""):
        self.name = name #name of sartist
        self.instrument = instrument #instruments played by artist
        self.bandList = [] #stores list of all the bands to which the artist belongs
    
    def setName(self, name): #setter
        self.name = name
    
    def setInstrument(self, instrument): #setter
        self.instrument = instrument
    
    def hasBand(self, arg_band): #check if artist belongs to a band
        if(isinstance(arg_band, Band)):
            return arg_band in self.bandList
    
    def addBand(self, arg_band): #link artist with band
        if(isinstance(arg_band, Band)):
            self.bandList.append(arg_band)
    
    def __str__(self): #toString()
        returnString =  self.name + " is a " + self.instrument + " and is in " + str(len(self.bandList)) + " band(s) {"
        for i in self.bandList:
            returnString += str(i.name) + ", "
        return returnString + "}";
    
    def __eq__(self, other): #override equality operator
        if isinstance(other, Artist):
            return self.name.lower() == other.name.lower()
        return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result    

#band entity    
class Band:
    def __init__(self, name=""):
        self.name = name
        self.artistList = [] #list of all artists in each band
    
    def setName(self, name):
        self.name = name
    
    def hasArtist(self, arg_artist): #check if an artist is part of the band
        if(isinstance(arg_artist, Artist)):
            return arg_artist in self.artistList
    
    def addArtist(self, arg_artist): #link artist with band
        if(isinstance(arg_artist, Artist)):
            self.artistList.append(arg_artist)
    
    def __str__(self): #toString()
        returnString = self.name + " has " + str(len(self.artistList)) + " member(s)"
        for i in self.artistList:
            returnString +=  "\n\t -> "+str(i)
        return returnString
    
    def getArtistArray(self): #getter, old habits dont die :(
        return self.artistList
    
    def __eq__(self, other): #override equality operator
        if isinstance(other, Band):
            return self.name.lower() == other.name.lower()
        return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result    


 #band manager manages bands and artists, linking and such like.
class BandManager:
    artistList = [] #maintain list of artists
    BandList = [] #maintain list of bands
    
    vizBandBackgroundColor = "black"
    vizBandFontColor = "white"
    vizBandShape = "egg"

    vizArtistBackgroundColor = "gray"
    vizArtistFontColor = "black"
    vizArtistShape = "ellipse"
    
    vizBackground = "white"
    vizArrowColor = "blue4"
    
    #graphViz attributes, edit this according to your taste
        
    def addArtist(self, arg_artist, instrument=""): #add artist to manager
        if(isinstance(arg_artist,Artist)): #make sure it's an artist
            if arg_artist in self.artistList: #if artist already exists in list
                    artistIndex = self.artistList.index(arg_artist)
                    if not str(arg_artist.instrument).strip() == "":
                        self.artistList[artistIndex].instrument = arg_artist.instrument #update instruments if needed
            else:
                self.artistList.append(arg_artist) #add artist to list
        else:
            if(isinstance(arg_artist,str)): #if called with string, make artist and recall
                self.addArtist(Artist(arg_artist,instrument))

    def bandExists(self, bandString): #check if band exists in list
        bandVar = Band(bandString)
        return bandVar in self.BandList

    def artistExists(self, artistString): #check if artist exists in list
        artistVar = Artist(artistString)
        return artistVar in self.artistList
    
    def addBand(self, arg_band):
        if(isinstance(arg_band,Band)): #make sure the argument is a band
            if not arg_band in self.BandList: #make sure band doesnt already exist
                self.BandList.append(arg_band)
        else:
            if(isinstance(arg_band,str)): #create a Band object and recall
                self.addBand(Band(arg_band))

    def link(self,artist, band): #link artist and band
        if(isinstance(band,Band)):
            if(isinstance(artist,Artist)): #make sure they are right datatypes

                #link band with artist
                if artist in self.artistList:
                    artistIndex = self.artistList.index(artist)
                    if not self.artistList[artistIndex].hasBand(band): #not already linked
                        self.artistList[artistIndex].addBand(band) #link
                else: #band not found
                    #create and recall
                    self.addArtist(artist);
                    self.link(artist,band);
                    return;
                
                #link artist with band
                if band in self.BandList:
                    bandIndex = self.BandList.index(band)
                    if not self.BandList[bandIndex].hasArtist(artist): #check if not already linked
                        self.BandList[bandIndex].addArtist(artist) #link
                else:
                    #create band and recall
                    self.addBand(band);
                    self.link(artist,band);
            else:
                print "\t\t[-] WRONG DATATYPE SENT TO LINK"
        else:
            print "\t\t[-] WRONG DATATYPE SENT TO LINK"

    def printAllArtists(self):
        returnString =""
        for i in self.artistList:
            returnString +=  str(i) + "\n"
        return returnString   

    def printAllBands(self):
        returnString =""
        for i in self.BandList:
            returnString +=  str(i) + "\n"
        return returnString

    def generateGV(self): #Generate GraphViz dot file.
        vizHeader = "digraph prof {"
        vizHeader = vizHeader  + "\n\tgraph [fontsize = \"20\", label = \"generated with bandViz\",size = \"60\", overlap=false, ratio = auto, bgcolor=\""+ self.vizBackground +"\"];"
        vizHeader = vizHeader + "\n\tnode [style=filled,fontsize = \"16\",size=\"30\",overlap=false];\n"
        filename = "bandviz.gv"
        file = open(filename, 'w')
        file.write(vizHeader) #write header
        for bandsIter in self.BandList:
            if bandsIter.artistList:
                bandString = "\"" + bandsIter.name + "\" " + "[shape=\""+self.vizBandShape+"\",style=\"filled\",color=\""+self.vizBandBackgroundColor+"\",fontcolor=\""+ self.vizBandFontColor+ "\" ];"
                file.write("\n\t" + bandString )
            
        for artistIterator in self.artistList:
            for bandIterator in artistIterator.bandList: #iterate and write data
                artistString = "\"" + artistIterator.name + "\" " + "[shape=\""+self.vizArtistShape+"\",style=\"filled\",color=\""+self.vizArtistBackgroundColor+"\",fontcolor=\""+ self.vizArtistFontColor+ "\" ];"
                file.write("\n\t" + artistString )
                file.write("\n\t\"" + str(artistIterator.name) + "\" -> \"" + str(bandIterator.name) + "\" [color=\""+ self.vizArrowColor + "\"];")
        file.write("\n}")
        file.close()        
        

if __name__ == '__main__':
    bm = BandManager()
    
    """
    bm.addArtist("Serj Tankian","Vocalist")
    bm.addArtist("Tom Morello","Guitarist")
    brad = Artist("Brad Wilk","Drummer")
    bm.addArtist(brad)
    bm.addBand("Rage Against The Machine")
    bm.addBand("The Night Watchman")
    audioslave = Band("Audioslave")
    bm.addBand(audioslave)
    """
    
    print "----------------LINKING-------------------------------"    
    bm.link(Artist("Tom Morello", "Guitarist"), Band("Audioslave"))
    bm.link(Artist("Tom Morello", "Guitarist"), Band("The Night Watchman"))
    bm.addArtist(Artist("Tom Morello", "_"))
    bm.addArtist(Artist("Tom Morello", " "))
    bm.addArtist(Artist("Tom Morello"))
    bm.addArtist("Tom Morello")
    bm.addBand("Jackson 5")
    bm.addBand("Jackson 5")
    bm.link(Artist("Sr", "Guitarist"), Band("Rage"))
    bm.link(Artist("Brad Wilk", "Drummer"), Band("Rage Against The Machine"))

    print "----------------PRINTING-------------------------------"    
    print bm.printAllArtists()
    print bm.printAllBands()

    print "----------------GENERATING-------------------------------"        
    bm.generateGV()
    print "-----------------------------------------------------"    
    
    #prune factor - cut out acts with less than 2 links
    #depth factor - recursion cut off
    #artist to album or (album to artist)
    #name of output file
