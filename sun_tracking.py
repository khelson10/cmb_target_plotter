# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:20:59 2015

@author: Laptop-23950
"""

import ephem as pe
import numpy as np
import healpy as hp

my_location = pe.Observer()
my_location.lon = '-68.2' #longitude, latitude and elevation of San Pedro de Atacama
my_location.lat = '-23'
my_location.elevation = 5000
NSIDE = 8
m = np.zeros(hp.nside2npix(NSIDE))
#%%
def findTarget(NSIDE, ra, dec, location):
    
    target = pe.FixedBody()
    target._ra = ra
    target._dec = dec
    
    ra = []
    dec = []
    
    for n in range(24*60):
        my_location.date += pe.minute
        target.compute(my_location)
        ra.append((target.ra))
        dec.append((target.dec))
        n += 1
    phi = ra
    theta = [np.pi/2 - i for i in dec]
    heal_index = hp.ang2pix(NSIDE, theta, phi)

    return heal_index
#%%

# taurus A 
TauA_ra = 8
TauA_dec = -47.5
TauA_heal_index = findTarget(NSIDE, TauA_ra, TauA_dec, my_location)
m[TauA_heal_index] = 1 

#RCW38
RCW38_ra = 5.51
RCW38_dec = 22.0
RCW38_heal_index = findTarget(NSIDE, RCW38_ra, RCW38_dec, my_location)
m[RCW38_heal_index] = 2


#Cen A
CenA_ra = 13.5
CenA_dec = -43
CenA_heal_index = findTarget(NSIDE, CenA_ra, CenA_dec, my_location)
m[CenA_heal_index] = 4
 

hp.mollview(m, coord = ['G','E'])