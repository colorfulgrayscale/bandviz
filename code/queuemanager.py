#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""

from wikiparser import WikiParser
from collections import deque
from bandmanager import *

class QueueManager: #manager recursion queue
    artistQueue=deque() #queue of artists
    bandQueue=deque() #queue of bands
    maxGlyphs = 10 #resolution of data
    glyphCounter = 0 #current resolution
    bm = BandManager() #init band manager
    expansiveArtistGraph = False #if enabled, will follow artist links with increased priority
    
    def __init__(self, link="http://en.wikipedia.org/wiki/Soundgarden"):
        self.addtoStack(link)        

    def addtoStack(self, link): #add band or artist to respective queue
        wparse = WikiParser(link)
        wmembers = wparse.getBandMembers()
        initialEntry = dict()
        if wmembers: #if band, add to band queue
            initialEntry["band"] = wparse.getName()
            initialEntry["link"] = link
            self.bandQueue.appendleft(initialEntry)
        else: #if artist add to artist queue
            initialEntry["artist"] = wparse.getName()
            initialEntry["link"] = link
            self.artistQueue.appendleft(initialEntry)
            
    def processArtists(self): 
        tempArtist = self.artistQueue.pop() #get top element
        if not self.expansiveArtistGraph:
            if self.bm.artistExists(tempArtist["artist"]): #artist already visited
                return 
        print "[a] - " + str(tempArtist["artist"]).strip()
        self.bm.addArtist(Artist(tempArtist["artist"])) #add artist to band manager
        if tempArtist["link"].strip() == "": #if has no follow link, break function
            return
        parser = WikiParser(tempArtist["link"])
        associatedActs = parser.getRelatedActs()
        for act in associatedActs : #add all associated acts to end of queue
            if not self.bm.bandExists(act["band"]):
                self.bandQueue.appendleft(act)

    def processBands(self):
        tempBand = self.bandQueue.pop() #get top element
        if tempBand["link"].strip() == "": #if has no follow link, break function
            return
        parser = WikiParser(tempBand["link"])
        members = parser.getBandMembers()
        formerMembers = parser.getBandMembers("former")
        for member in members: 
            self.artistQueue.appendleft(member) #add member artists to artist stack
            self.bm.link( Artist(member["artist"]), Band(tempBand["band"])) #link band with artist
        if not members and not formerMembers: #if artist accidentaly ends up in band, add back to artist.
            artistEntry = dict()
            artistEntry["artist"] = tempBand["band"]
            artistEntry["link"] = tempBand["link"]
            self.artistQueue.appendleft(artistEntry)
            return
        print "[b] - " + str(tempBand["band"]).strip()
        self.bm.addBand(tempBand["band"])
        associatedActs = parser.getRelatedActs()
        for act in associatedActs : #add all associated acts to end of queue
            if not self.bm.bandExists(act["band"]):
                self.bandQueue.appendleft(act)
            
    def hasMoreElements(self): #determines if any elements are left in stack
        if self.artistQueue:
            return True
        if self.bandQueue:
            return True
        return False
        
    def printbandQueue(self):
        print "\n\n+=+=+=+=+=+==+=+=+==+=+=+=+=BAND STACK+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==\n"
        for item in self.bandQueue:
            print  str(item)
        print "\n--------------------------------------BAND LIST---------------------\n"
        print self.bm.printAllBands()
        print "\n+=+=+=+=+==+=+=+==+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==+=+=+=+=+=+=\n\n"                    

    def printartistQueue(self):
        print "\n\n+=+=+=+=+=+==+=+=+==+=+=+=+=artist STACK+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==\n"
        for item in self.artistQueue:
            print  str(item)
        print "\n--------------------------------------artist LIST---------------------\n"
        print self.bm.printAllArtists()
        print "\n+=+=+=+=+==+=+=+==+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+==+=+=+=+=+=+=\n\n"                    

    def start(self,resolution=10):
        self.maxGlyphs = resolution
        while self.hasMoreElements():
            if not self.glyphCounter  == self.maxGlyphs:
                self.glyphCounter = self.glyphCounter+1                
                if self.artistQueue:
                    #self.printartistQueue()
                    self.processArtists()
                if self.bandQueue:
                    #self.printbandQueue()
                    self.processBands()
            else:
                print "\n\n[-] Stopping, Resolution reached.\n"
                break
        self.bm.generateGV()
            
    