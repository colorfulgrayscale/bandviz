#!/usr/bin/env python

from wikiparser import WikiParser
from bandmanager import *
import pprint

class StackManager:
    artistStack=[]
    bandStack=[]
    def __init__(self, link="http://en.wikipedia.org/wiki/Soundgarden"):
        
        wparse = WikiParser(link)
        wnameArtist = wparse.getName("artist")
        wnameBand = wparse.getName("band")
        initialEntry = {'':''} #init dictionary
        if wnameArtist.strip()=="":
            initialEntry[wnameBand] = link
            self.bandStack.append(initialEntry)
        else:
            if wnameBand.strip()=="":
                initialEntry[wnameArtist] = link
                self.artistStack.append(initialEntry)
    
    def processArtists(self):
        tempArtist = self.artistStack.pop()
        print "\nARTIST === " + str(tempArtist) 

    def processBands(self):
        tempBand = self.bandStack.pop()
        print "\nband === " + str(tempBand)
        print "\n"
        pprint.pprint(tempBand)

        #for i in tempBand:
        #    print "\n\t\t" + str(i)
        
            
    def hasMoreElements(self):
        if self.artistStack:
            return True
        if self.bandStack:
            return True
        return False
        
                    
    def start(self):
        while self.hasMoreElements():
            if self.artistStack: self.processArtists()
            if self.bandStack: self.processBands()
    


stack = StackManager("http://en.wikipedia.org/wiki/Soundgarden")


print stack.start()