# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:20:59 2015

@author: Laptop-23950
"""

import ephem as pe
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

my_location = pe.Observer()
my_location.lon = '-68.2' #longitude, latitude and elevation of San Pedro de Atacama
my_location.lat = '-23'
my_location.date = '2018/1/1 0:00'
my_location.elevation = 5000
NSIDE = 512
m = np.zeros(hp.nside2npix(NSIDE))
# download the Planck LFI Sky Map at 44 GHz and place it locally in your own dir
planck_path = './LFI_SkyMap_044_1024_R2.01_full.fits'
m = hp.read_map(planck_path,field = 1)


#%%
def findTarget(NSIDE, ra, dec, location):
    
    target = pe.FixedBody()
    target._ra = ra
    target._dec = dec
    
    ra = []
    dec = []
    
    for n in range(24*60):
        my_location.date += pe.minute
        target.compute(location)
        ra.append((target.ra))
        dec.append((target.dec))
        n += 1

    phi = ra
    theta = [np.pi/2 - i for i in dec]

    return target, np.mean(phi), np.mean(theta)
#%%

# taurus A 
#RA 05 34 31.94 
#DEC +22 00 52.2
TauA_ra = 5.0 + (34.0/60) + (31.94/3600)
TauA_dec = 22.0 + (52.2/3600)
TauA_target,TauA_phi, TauA_theta = findTarget(NSIDE, TauA_ra, TauA_dec, my_location)

#RCW38
#RA 08 59 05.50
#DEC -47 30 39.4
RCW38_ra = 8.0+(59.0/60)+(5.5/3600)
RCW38_dec = -(47.0 + 30.0/60 + 39.4/3600)
RCW38_target, RCW38_phi, RCW38_theta = findTarget(NSIDE, RCW38_ra, RCW38_dec, my_location)

#Cen A
#RA 13 25 27.6
#Dec - 43° 01′ 09″
CenA_ra = 13.0 + (25.0/60) + (27.6/3600)
CenA_dec = -(43.0 + 1.0/60 + 9.0/3600)
CenA_target, CenA_phi, CenA_theta = findTarget(NSIDE, CenA_ra, CenA_dec, my_location)

#%% 


x = np.array([TauA_theta, RCW38_theta, CenA_theta])
y = np.array([TauA_phi, RCW38_phi, CenA_phi])
names = ['Tau A', 'RCW38', 'Cen A']
hp.mollview(m, coord = ['G','E'], norm = 'hist')
hp.projscatter(x, y, coord=['G'], color = 'red')
[hp.projtext(x[i], y[i]-0.2, names[i], color = 'red',size = 'x-large', coord = ['G','E']) for i in range(3)]

hp.graticule()

#%%


TauA_pixels = hp.query_disc(NSIDE,hp.ang2vec(TauA_theta, TauA_phi), np.pi/90)
CenA_pixels = hp.query_disc(NSIDE,hp.ang2vec(CenA_theta, CenA_phi), np.pi/90)
RCW38_pixels = hp.query_disc(NSIDE,hp.ang2vec(RCW38_theta, RCW38_phi), np.pi/90)
plt.figure(2)
plt.plot(m[TauA_pixels])
plt.plot(m[CenA_pixels])
plt.plot(m[RCW38_pixels])
plt.show()






