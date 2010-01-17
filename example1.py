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

#you'll need to get the wikipedia link for the artist/band and call QueueManager with it.
queueManager = queuemanager.QueueManager("http://en.wikipedia.org/wiki/Rage_Against_the_Machine")

queueManager.bm.vizBandBackgroundColor = "gray43"
queueManager.bm.vizBandShape = "egg" #for complete list of shapes goto http://www.graphviz.org/doc/info/shapes.html
queueManager.bm.vizBandFontColor = "white"
queueManager.bm.vizArtistBackgroundColor = "gray"
queueManager.bm.vizArtistShape = "ellipse"
queueManager.bm.vizArtistFontColor = "black"
queueManager.bm.vizBackground = "white"
queueManager.bm.vizArrowColor = "gray43" #for complete list of names goto http://www.graphviz.org/doc/info/colors.html
queueManager.expansiveArtistGraph = False #enable this if you want to increase priority of fetching artists

queueManager.start(10) #call with resolution as parameter, higher this integer value takes longer and produces bigger and more exhaustive graphs
