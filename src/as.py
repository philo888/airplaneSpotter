#!/usr/bin/python

#
#
# Program je nutne spouste s parametrem jmana letu nebo jeho hex
# Vyzaduje spusteny SW dump 1090
#

import sys
import urllib
import json
import ephem
import math
import time

obsPlace = ephem.Observer()
obsPlace.lon = '14:28.073'
obsPlace.lat = '48:59.229'
obsPlace.elevation = 350.0

ObsLon =  14+28.073/60
ObsLat =  48+59.229/60
ObsAlt =  350.0

R = 6371.0

print ObsLon, ObsLat, ObsAlt

aimAirplane = "ROT36BR"         # jmeno letu, nebo jeho hex
aimAirplane = sys.argv[1]
print aimAirplane

url = "http://telescopeC.local:8080/data.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
for airplane in data:
	print "airplane:", airplane

print ""

while True:
	time.sleep(0.5)
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	for airplane in data:
	#if True:
		if aimAirplane in airplane['flight'] or  aimAirplane in airplane['hex']:
		#if True:
			
			myplane = airplane
			PlaneLon = myplane['lon']
			PlaneLat = myplane['lat']
			PlaneAlt = myplane['altitude']*0.3048 #ft
			

			dlon = math.radians(PlaneLon) - math.radians(ObsLon )
			dlat = math.radians(PlaneLat) - math.radians(ObsLat )

			a = math.sin(dlat/2)*math.sin(dlat/2) + (math.cos(math.radians(ObsLat)) * math.cos(math.radians(PlaneLat)) * math.sin(dlon/2)* math.sin(dlon/2)) 
			c = 2 * math.asin(min(1,math.sqrt(a))) 
			d = R * c


			lat1 = math.radians(ObsLat)
			lat2 = math.radians(PlaneLat)
			x = math.sin(dlon) * math.cos(lat2)
			y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
			initial_bearing = math.atan2(x, y)
			initial_bearing = math.degrees(initial_bearing)
			az = (initial_bearing + 360) % 360

			alt = (180.0/math.pi) * ( (PlaneAlt - ObsAlt) / d - d / (2.0*R*1000) )



			print "myplane", PlaneLat, PlaneLon, PlaneAlt, "distance", d, "azimuth", az, "alt", alt, "\r",
