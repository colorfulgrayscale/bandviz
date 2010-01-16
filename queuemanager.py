#!/usr/bin/env python

from wikiparser import WikiParser
from collections import deque
from bandmanager import *
import os

class QueueManager:
    artistStack=deque()
    bandStack=deque()
    maxGlyphs = 10
    glyphCounter = 0
    bm = BandManager()
    
    def __init__(self, link="http://en.wikipedia.org/wiki/Soundgarden"):
        self.addtoStack(link)        

    def addtoStack(self, link):
        wparse = WikiParser(link)
        wmembers = wparse.getBandMembers()
        initialEntry = dict()
        if wmembers:
            initialEntry["band"] = wparse.getName()
            initialEntry["link"] = link
            self.bandStack.appendleft(initialEntry)
        else:
            initialEntry["artist"] = wparse.getName()
            initialEntry["link"] = link
            self.artistStack.appendleft(initialEntry)
            
    def processArtists(self):
        tempArtist = self.artistStack.pop()
        print "\nARTIST === " + str(tempArtist)
        print "\n"
        self.bm.addArtist(Artist(tempArtist["artist"]))
        if tempArtist["link"].strip() == "":
            return
        
        parser = WikiParser(tempArtist["link"])
        associatedActs = parser.getRelatedActs()
        for act in associatedActs :
            if not self.bm.bandExists(act["band"]):
                print "** Adding band to stack " + str(act)
                self.bandStack.appendleft(act)
            else:
                print "\n ** Skipping Adding band to stack " + str(act)
        

    def processBands(self):
        tempBand = self.bandStack.pop()
        print "\nband === " + str(tempBand)
        print "\n"
        self.bm.addBand(tempBand["band"])
        if tempBand["link"].strip() == "":
            return
        parser = WikiParser(tempBand["link"])
        members = parser.getBandMembers()
        print "--> Members\n "
        for member in members:
            print "\n---->" + str(member) + "\n"
            self.artistStack.appendleft(member)
            self.bm.link( Artist(member["artist"]), Band(tempBand["band"]))
            
        if not members:
            print "\n===> NO MEMBERS FOUND, MOVING TO ARTIST "
            artistEntry = dict()
            artistEntry["artist"] = tempBand["band"]
            artistEntry["link"] = tempBand["link"]
            self.artistStack.appendleft(artistEntry)
            return
            
        associatedActs = parser.getRelatedActs()
        for act in associatedActs :
            if not self.bm.bandExists(act["band"]):
                print "** Adding band to stack " + str(act)
                self.bandStack.appendleft(act)
            else:
                print "\n ** Skipping Adding band to stack " + str(act)
            
    def hasMoreElements(self):
        if self.artistStack:
            return True
        if self.bandStack:
            return True
        return False
        
    def printBandStack(self):
        print "\n\n+=+=+=+=+=+==+=+=+==+=+=+=+=BAND STACK+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==\n"
        for item in self.bandStack:
            print  str(item)
        print "\n--------------------------------------BAND LIST---------------------\n"
        print self.bm.printAllBands()
        print "\n+=+=+=+=+==+=+=+==+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==+=+=+=+=+=+=\n\n"                    

    def printArtistStack(self):
        print "\n\n+=+=+=+=+=+==+=+=+==+=+=+=+=artist STACK+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==\n"
        for item in self.artistStack:
            print  str(item)
        print "\n--------------------------------------artist LIST---------------------\n"
        print self.bm.printAllArtists()
        print "\n+=+=+=+=+==+=+=+==+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==+=+=+=+=+=+=\n\n"                    


    def start(self):
        while self.hasMoreElements():
            if not self.glyphCounter  == self.maxGlyphs:
                self.glyphCounter = self.glyphCounter+1                
                if self.artistStack:
                    self.printArtistStack()
                    self.processArtists()
                if self.bandStack:
                    self.printBandStack()
                    self.processBands()
                    
                    
            else: break
    

os.system("clear")

qm = QueueManager("http://en.wikipedia.org/wiki/Tool_(band)")
qm.start()
qm.bm.generateGV()