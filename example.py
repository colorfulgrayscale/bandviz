#!/usr/bin/env python

"""
bandViz
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""

import os
from code import queuemanager

os.system("clear")

bandViz = queuemanager.QueueManager() #initialize bandViz

#add artist/bands to queue
bandViz.addtoQueue("http://en.wikipedia.org/wiki/Nine_Inch_Nails")

#name of output graphViz file
bandViz.bm.vizOutpuFileName = "example.gv" 

#graph colors and properties.
#complete list of colors @ http://www.graphviz.org/doc/info/colors.html
#complete list of node shapes @ http://www.graphviz.org/doc/info/shapes.html
bandViz.bm.vizBackground = "gray90"
bandViz.bm.vizArrowColor = "gray43" 
bandViz.bm.vizBandBackgroundColor = "gray43"
bandViz.bm.vizBandShape = "egg" 
bandViz.bm.vizBandFontColor = "white"
bandViz.bm.vizArtistBackgroundColor = "gray"
bandViz.bm.vizArtistShape = "ellipse"
bandViz.bm.vizArtistFontColor = "black"

#enable this to make it show defunct members of band and defunct bands.
#enabling this will your graph bigger.
bandViz.showFormerMembers = False 

#enable this if you want to increase priority of fetching artists.
#enabling this will follow every artist link, ie. it increases your queue size.
bandViz.expansiveArtistGraph = False 

#resolution. Increase this to increase the size of your graph
#warning: higher resolutions take longer
bandViz.resolution = 10

#enable printDebug to make bandViz print the entity its currently processing
#onto the console
bandViz.printDebug = True

#start the process! It returns a int with time elapsed
totalTime = bandViz.start() 

#show time elapsed
min = round(totalTime/60,1)
print "\nFinished in " + str(totalTime) + " seconds. (" + str(min) + " mins)\n"
print "Graphviz file written to 'example.gv'\n"