# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 15:58:00 2015

@author: krostem
"""

from ephem import *


#m = Mars('1983')
#print(constellation(m))


#j = Jupiter()
#j.compute('1986/2/8')
#print('%s %s' % (j.ra, j.dec))
#j.compute('1986/2/9', epoch='1950')
#print('%s %s' % (j.a_ra, j.a_dec))




gatech = Observer()
gatech.lon = '-84.39733'
gatech.lat = '33.775867'
gatech.elevation = 5000 #in meters
gatech.date = '2015/15/9 15:00:00'
j = Jupiter()
j.compute(gatech)

#print('%s' % (CircumpolarError(j)))


print(gatech.next_transit(j))
print('%s %s' % (j.alt, j.az))

#print(j.circumpolar)

#v = Venus(gatech)
#print('%s %s' % (v.alt, v.az))


#%%

#this gives weird results... the sun should be at 180deg at 12pm local time

gatech = Observer()
gatech.lon = '0'
gatech.lat = '30'
gatech.elevation = 320
gatech.date = '1984/6/30 08:59:4'
s = Sun(gatech)
gatech.epoch = J2000
print('%s %s' % (s.alt, s.az))
print(localtime(gatech.date))
print(gatech.next_transit(s))