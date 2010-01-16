#!/usr/bin/env python

class Artist:
    def __init__(self, name="",instrument=""):
        self.name = name
        self.instrument = instrument
        self.bandList = [] #stores list of all bands the artist is in
    def setName(self, name):
        self.name = name
    def setInstrument(self, instrument):
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
    
class Band:
    def __init__(self, name=""):
        self.name = name
        self.artistList = [] #list of all artists in each band
    def setName(self, name):
        self.name = name
    def hasArtist(self, arg_artist):
        if(isinstance(arg_artist, Artist)):
            return arg_artist in self.artistList
    def addArtist(self, arg_artist):
        if(isinstance(arg_artist, Artist)):
            self.artistList.append(arg_artist)
    def __str__(self):
        returnString = self.name + " has " + str(len(self.artistList)) + " member(s)"
        for i in self.artistList:
            returnString +=  "\n\t -> "+str(i)
        return returnString
    def getArtistArray(self):
        return self.artistList
    def __eq__(self, other):
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
    artistList = []
    BandList = []
    vizHeader = "digraph prof {\n\tsize=\"6,4\";\n\tratio = fill;\n\tnode [style=filled];"

    def addArtist(self, arg_artist, instrument=""):
        
        if(isinstance(arg_artist,Artist)):
            if arg_artist in self.artistList:
                    artistIndex = self.artistList.index(arg_artist)
                    if str(arg_artist.instrument).strip() == "":
                        print "* Skipping Create New Artist " + str(arg_artist.name) + ", already exists at index:" + str(artistIndex)
                    else:
                        print "* Updated instrument for Artist " + str(arg_artist.name) + ", replaced " + str(self.artistList[artistIndex].instrument) + " with " + str(arg_artist.instrument)  
                        self.artistList[artistIndex].instrument = arg_artist.instrument
            else:
                self.artistList.append(arg_artist)
                print "* Creating New Artist " + str(arg_artist.name) + ", " + str(arg_artist.instrument)
        else:
            if(isinstance(arg_artist,str)):
                self.addArtist(Artist(arg_artist,instrument))

    def bandExists(self, bandString):
        bandVar = Band(bandString)
        if bandVar in self.BandList:
            return True
        else:
            return False

    def artistExists(self, artistString):
        artistVar = Artist(artistString)
        if artistVar in self.artistList:
            return True
        else:
            return False
    
    def addBand(self, arg_band):
        if(isinstance(arg_band,Band)):
            if arg_band in self.BandList:
                    bandIndex = self.BandList.index(arg_band)
                    print "# Skipping Create New Band " + str(arg_band.name) + ", already exists at index:" + str(bandIndex)
            else:
                self.BandList.append(arg_band)
                print "# Creating New Band " + str(arg_band.name)
        else:
            if(isinstance(arg_band,str)):
                self.addBand(Band(arg_band))

    def link(self,artist, band):
        print "\t -> Trying to Link " + artist.name +" with " +  band.name
        if(isinstance(band,Band)):
            if(isinstance(artist,Artist)):
                #link band with artist
                if artist in self.artistList:
                    artistIndex = self.artistList.index(artist)
                    if not self.artistList[artistIndex].hasBand(band):
                        self.artistList[artistIndex].addBand(band)
                        print "\t\tLinking artist " + self.artistList[artistIndex].name + " with band " + band.name;                        
                    else:
                        print "\t\tArtist " + self.artistList[artistIndex].name + " has already been linked to band " + band.name + ", skipping";    
                else:
                    #create mode
                    print "\t\tArtist " + artist.name + " not found, Creating Artist, Relinking";                    
                    self.addArtist(artist);
                    self.link(artist,band);
                    return;
                #link artist with band
                if band in self.BandList:
                    bandIndex = self.BandList.index(band)
                    if not self.BandList[bandIndex].hasArtist(artist):
                        self.BandList[bandIndex].addArtist(artist)
                        print "\t\tLinking band " + self.BandList[bandIndex].name + " with artist " + artist.name;                                                
                    else:
                        print "\t\tBand " + self.BandList[bandIndex].name + " has already been linked to artist " + artist.name;                                                
                else:
                    #create mode
                    print "\t\tBand " + band.name + " not found, creating Band, Relinking";                                                
                    self.addBand(band);
                    self.link(artist,band);
            else:
                print "\t\t!! WRONG DATATYPE ||"
        else:
            print "\t\t!! WRONG DATATYPE !!"

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

    def generateGV(self):
        filename = "bandviz.gv"
        file = open(filename, 'w')
        file.write(self.vizHeader)
        for artistIterator in self.artistList:
            print ">> " + str(artistIterator.name)
            for bandIterator in artistIterator.bandList:
                print  "   + " +  str(bandIterator.name)
                file.write("\n\t\"" + str(artistIterator.name) + "\" -> \"" + str(bandIterator.name) + "\" [color=\"0.650 0.700 0.700\"];")
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
    
    
    