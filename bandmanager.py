#!/usr/bin/env python

class Artist:
    def __init__(self, name="",instrument=""):
        self.name = name
        self.instrument = instrument
        self.bandList = []
    def setName(self, name):
        self.name = name
    def setInstrument(self, instrument):
        self.instrument = instrument
    def hasBand(self, arg_band):
        if(isinstance(arg_band, Band)):
            return arg_band in self.bandList
    def addBand(self, arg_band):
        if(isinstance(arg_band, Band)):
            self.bandList.append(arg_band)
    def __str__(self):
        returnString =  self.name + " is a " + self.instrument + " and is in " + str(len(self.bandList)) + " band(s) {"
        for i in self.bandList:
            returnString += str(i.name)
        return returnString + "}";
    def __eq__(self, other):
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
        self.artistList = []
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
    def __eq__(self, other):
        if isinstance(other, Band):
            return self.name.lower() == other.name.lower()
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result    


class BandManager:
    artistList = []
    BandList = []
    def addArtist(self, arg_artist, instrument=""):
        if(isinstance(arg_artist,Artist)):
            self.artistList.append(arg_artist)
        else:
            if(isinstance(arg_artist,str)):
                self.artistList.append(Artist(arg_artist,instrument))

    def addBand(self, arg_band):
        if(isinstance(arg_band,Band)):
            self.BandList.append(arg_band)
        else:
            if(isinstance(arg_band,str)):
                self.BandList.append(Band(arg_band))
                
    def link(self,artist, band):
        print "\t -> Trying to Link " + artist.name +" with " +  band.name
        if(isinstance(band,Band)):
            if(isinstance(artist,Artist)):

                #link band with artist
                if artist in self.artistList:
                    artistIndex = self.artistList.index(artist)
                    if not self.artistList[artistIndex].hasBand(band):
                        self.artistList[artistIndex].addBand(band)
                        print "\t\t Linked artist " + self.artistList[artistIndex].name + " with band " + band.name;                        
                    else:
                        print "\t\tArtist " + self.artistList[artistIndex].name + " has already been linked to band " + band.name + ", skipping";    
                else:
                    #create mode
                    print "\t\tArtist " + artist.name + " not found, Creating Artist, Relinking";                    
                    self.addArtist(artist);
                    self.link(artist,band);
                
                #link artist with band
                if band in self.BandList:
                    bandIndex = self.BandList.index(band)
                    if not self.BandList[bandIndex].hasArtist(artist):
                        self.BandList[bandIndex].addArtist(artist)
                        print "\t\t Linked band " + self.BandList[bandIndex].name + " with artist " + artist.name;                                                
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
        

if __name__ == '__main__':
    print "Making..."
    bm = BandManager()
    bm.addArtist("Serj Tankian","Vocals")
    bm.addArtist("Tom Morello","Guitarist")
    brad = Artist("Brad Wilk","Drummer")
    bm.addBand("Rage Against The Machine")
    audioslave = Band("Audioslave")
    bm.addBand(audioslave)
    bm.addArtist(brad)
    print "test printing..."    
    print bm.printAllArtists()
    print bm.printAllBands()
    print "-----------------------------------------------"    
    print "linking..."
    bm.link(Artist("Tom Morello", "Guitarist"), Band("Audioslave"))
    bm.link(Artist("Sr", "Guitarist"), Band("Rage"))
    bm.link(Artist("Brad Wilk", "Drummer"), Band("Rage Against The Machine"))
    print "-----------------------------------------------"        
    print bm.printAllArtists()
    print bm.printAllBands()


#bob.setInstrument("sdf")
#print bob
#
#sam = Band("Band 1");
#print sam;
#sam.addArtist(bob)
#
#bob.addBand(sam)
#print sam;
#print bob;