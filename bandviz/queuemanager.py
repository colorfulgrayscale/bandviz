#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""


import time
from collections import deque
from wikiparser import WikiParser
from bandmanager import *


class QueueManager: 
    """Wikipedia parser queue manager"""

    
    def __init__(self):
        """Constructor"""
        self.__artistQueue=deque() #queue of artists
        self.__bandQueue=deque() #queue of bands
        #default values
        self.resolution = 10 #resolution of data
        self.__glyphCounter = 0 #current resolution
        self.showFormerMembers = False #show/hide defunct members of band.
        self.bm = BandManager() #init band manager
        self.expansiveArtistGraph = False #enabled/disable follow artist links
        self.printDebug = False #enable/disable output to console

    def addtoQueue(self, link):
        """add band or artist to parse queue"""
        wparse = WikiParser(link)
        wmembers = wparse.getBandMembers()
        initialEntry = dict()
        if wmembers: #if band, add to band queue
            initialEntry["band"] = wparse.getName()
            initialEntry["link"] = link
            self.__bandQueue.appendleft(initialEntry)
        else: #if artist add to artist queue
            initialEntry["artist"] = wparse.getName()
            initialEntry["link"] = link
            self.__artistQueue.appendleft(initialEntry)
            
    def __processArtists(self):
        """manage artist queue"""
        tempArtist = self.__artistQueue.pop() #get top element
        if not self.expansiveArtistGraph: #check if to follow artist links
            #artist already visited
            if self.bm.artistExists(tempArtist["artist"]): 
                return 
        if self.printDebug: print "[a] - " + str(tempArtist["artist"]).strip()
        #add artist to band manager
        self.bm.addArtist(Artist(tempArtist["artist"])) 
        #if has no follow link, break function
        if tempArtist["link"].strip() == "": 
            return
        parser = WikiParser(tempArtist["link"])
        associatedActs = parser.getRelatedActs()
        for act in associatedActs : #add all associated acts to end of queue
            if not self.bm.bandExists(act["band"]):
                self.__bandQueue.appendleft(act)

    def __processBands(self):
        tempBand = self.__bandQueue.pop() #get top element
        #if has no follow link, break function
        if tempBand["link"].strip() == "": 
            return
        parser = WikiParser(tempBand["link"])
        members = parser.getBandMembers()
        formerMembers = parser.getBandMembers("former")            
        for member in members:
            #add member artists to artist stack
            self.__artistQueue.appendleft(member)
            #link band with artist
            self.bm.link( Artist(member["artist"]), Band(tempBand["band"])) 
        if(self.showFormerMembers):
            for member in formerMembers:
                #add member artists to artist stack
                self.__artistQueue.appendleft(member)
                #link band with artist
                self.bm.link( Artist(member["artist"]), Band(tempBand["band"]),True) 
        #if artist accidentaly ends up in band, add back to artist.
        if not members and not formerMembers: 
            artistEntry = dict()
            artistEntry["artist"] = tempBand["band"]
            artistEntry["link"] = tempBand["link"]
            self.__artistQueue.appendleft(artistEntry)
            return
        if self.printDebug: print "[b] - " + str(tempBand["band"]).strip()
        self.bm.addBand(tempBand["band"])
        associatedActs = parser.getRelatedActs()
        #add all associated acts to end of queue
        for act in associatedActs : 
            if not self.bm.bandExists(act["band"]):
                self.__bandQueue.appendleft(act)
            
    def __hasMoreElements(self):
        """Returns if the parse queues have elements"""
        if self.__artistQueue:
            return True
        if self.__bandQueue:
            return True
        return False

    def start(self):
        """Starts the parse process. Returns total time taken in secs."""
        start = time.time() #start time for elapsed time
        while self.__hasMoreElements():
            if not self.__glyphCounter  == self.resolution:
                self.__glyphCounter = self.__glyphCounter+1 #resolution counter
                if self.__artistQueue:
                    self.__processArtists()
                if self.__bandQueue:
                    self.__processBands()
            else:
                if self.printDebug:
                    print "\n[-] Stopping, Resolution reached.\n"
                break
        self.bm.generateGV(self.showFormerMembers)
        end = time.time()
        elapsed= round(end - start,1)
        return elapsed