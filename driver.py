#!/usr/bin/env python

import artist;
import band;

bob = artist.Artist("Bob Smith")
bob.setInstrument("sdf")
print bob

sam = band.Band("Band 1");
print sam;
sam.addArtist(bob)
print sam;



