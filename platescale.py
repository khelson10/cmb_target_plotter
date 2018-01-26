# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:19:58 2015

@author: mberkeley
"""
import ephem as pe
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp

x_offset = []
y_offset = []

filename = '40GHz_36Alpha_xAlpha_y3.dat'

#file contains offsets from center axis of the CLASS FOV
for line in open(filename, 'r'):
    az, el = line.split()
    x_offset.append(az)
    y_offset.append(el)
    
coords = zip(x_offset,y_offset)
#print coords

scan_rate = 0 #2 * np.pi / (24*60*60) #deg per sec

x_int = pe.minute
x_sample = np.arange(60*60*24) * x_int
start_date = pe.Date('2016/1/21 00:00:00')
x_date = start_date + x_sample

ra_arrs = []
dec_arrs = []


alt_center = 25. * np.pi / 180

pixelname = pe.Observer()
pixelname.lat = -22.959722
pixelname.lon = -67.787222
pixelname.date = start_date

for i in range(len(coords)):
    #assign vectors for RA and DEC
    ra_arr = np.zeros_like(x_sample)
    dec_arr = np.zeros_like(x_sample)
    az = float(x_offset[i])
    
    alt = alt_center + float(y_offset[i])
    for z in range(len(x_sample)):
        pixelname.date = pe.Date(x_date[z]) #UTC
        az_scan = az + scan_rate * float(z) 
        ra, dec = pixelname.radec_of(az_scan, alt)
        ra_arr[z] = (ra)
        dec_arr[z] = (dec)
    ra_arrs.append(ra_arr)
    dec_arrs.append(dec_arr)

#convert to healpix and plot...
#wait... healpy functions need DEC in the range 0,pi, so convert DEC
hp_decs = [np.pi / 2. - dec_arrs[j] for j in range(len(dec_arrs))]
print hp_decs

NSIDE = 128 #resolution of the map
npix = hp.nside2npix(NSIDE)

nhits_tot = np.zeros(npix)

for k in range(len(hp_decs)):
    healIndex = hp.ang2pix(NSIDE, hp_decs[k], ra_arrs[k]) #index in healpy - ring format
    nhits = np.bincount(healIndex,minlength=npix)
    nhits_tot += nhits

print nhits_tot
#show the map
hp.mollview(nhits_tot, title='Hit map')


'''
plt.figure()
plt.plot(azimuths,elevations,'r.')
plt.show()
'''

