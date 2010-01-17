#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""

from code import queuemanager
import os

os.system("clear")

queueManager = queuemanager.QueueManager("http://en.wikipedia.org/wiki/Rage_Against_the_Machine")

queueManager.bm.vizBandBackgroundColor = "black"
queueManager.bm.vizBandShape = "egg"
queueManager.bm.vizBandFontColor = "white"
queueManager.bm.vizArtistBackgroundColor = "gray"
queueManager.bm.vizArtistShape = "ellipse"
queueManager.bm.vizArtistFontColor = "black"
queueManager.bm.vizBackground = "white"
queueManager.bm.vizArrowColor = "blue4" #for complete list of names goto http://www.graphviz.org/doc/info/colors.html
queueManager.expansiveArtistGraph = False

queueManager.start(10) #call with resolution as parameter, higher resolution takes longer and produces bigger graphs
