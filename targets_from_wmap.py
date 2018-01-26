# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:31:04 2018

@author: khelson
"""

import ephem as pe
import numpy as np
import healpy as hp

my_location = pe.Observer()
my_location.lon = '-68.2' #longitude, latitude and elevation of San Pedro de Atacama
my_location.lat = '-23'
my_location.elevation = 5000

wmap_map = hp.read_map('/Users/khelson/Documents/CLASS/sky coordinates examples/wmap_band_iqumap_r9_9yr_Q_v5.fits')


NSIDE = 512

hp.mollview(wmap_map, coord = ['G','E'], norm = 'hist')
hp.graticule(dpar = 0.5, dmer = 0.5)
