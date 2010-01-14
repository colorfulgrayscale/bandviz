#!/usr/bin/env python
import artist

class Band:
    artistList = []
    def __init__(self, name=""):
        self.name = name
    def setName(self, name):
        self.name = name
    def addArtist(self, arg_artist):
        if(isinstance(arg_artist, artist.Artist)):
            self.artistList.append(artist)
    def __str__(self):
        returnString = self.name + " has " + str(len(self.artistList)) + " members ("
        for i in self.artistList:
            print i.name
            #returnString +=  + " "
        return returnString + ")"    


