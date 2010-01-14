#!/usr/bin/env python

class Artist:
    bandList = []
    def __init__(self, name="",instrument=""):
        self.name = name
        self.instrument = instrument
    def setName(self, name):
        self.name = name
    def setInstrument(self, instrument):
        self.instrument = instrument
    def addBand(self, arg_band):
        if(isinstance(arg_band, Band)):
            self.artistList.append(arg_band)
    def __str__(self):
        return self.name + " plays the " + self.instrument + " - " + str(len(self.bandList)) + " bands"
    def toString(self):
        return self.name + " plays the " + self.instrument + " - " + str(len(self.bandList)) + " bands"        
    

