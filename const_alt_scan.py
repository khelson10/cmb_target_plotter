# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:22:05 2015

@author: krostem
"""

import numpy as np
import ephem as pe
import healpy as hp
#import pylab as pl
#%%

#RCW38 RA/Dec

#Right ascension	 08 59 05.50
#Declination	-47 30 39.4




#%%


#create a vector containing all the azimuth, altitude, day, and time 
#set location
telescope = pe.Observer()
telescope.lon = '46.0' #somewhere in the old country
telescope.lat = '35.0'

#sample every X seconds on the sky
x_int = pe.second #sec
x_sample = np.arange(60*60) * x_int 
scan_rate = 360. / (24 * 60 * 60) #deg per sec

#assign vectors for RA and DEC
ra_arr = np.zeros_like(x_sample)
dec_arr = np.zeros_like(x_sample)

#set the start date/time of the observing session
telescope.date = pe.Date('2017/1/21 00:00:00') #UTC

x_date = telescope.date + x_sample

#define telescope altiude...
#alt = 0 
sun = pe.Sun()
for z in range(len(x_sample)):
    telescope.date = pe.Date(x_date[z]) #UTC

    #az_scan = 0. #scan_rate * float(z) 
    sun.compute(telescope)
    az, alt = sun.az, sun.alt
    ra, dec = telescope.radec_of(float(az), float(alt))
    ra_arr[z] = (sun.ra)
    dec_arr[z] = (sun.dec)
    print("%s %s" % (alt, az))

#%%

#convert to healpix and plot...
#wait... healpy functions need DEC in the range 0,pi, so convert DEC
hp_dec = np.pi / 2. - dec_arr

NSIDE = 128 #resolution of the map
npix = hp.nside2npix(NSIDE)

healIndex = hp.ang2pix(NSIDE, hp_dec, ra_arr) #index in healpy - ring format
nhits = np.bincount(healIndex,minlength=npix)

#show the map
hp.mollview(nhits, title='Hit map')

