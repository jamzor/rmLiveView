#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ COMPUTE.PY ~
#   @author:    james macisaac
#   @created:   July 4th, 2016
#   @updated:   July 2016
#   @project:   Live View
#   @desc:      This file manages the methods which compute values, or 
#               satisfy a logical purpose in the underlying application.
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

import re

#****************************************************************************
#   PARSING METHODS
#   @author:    james macisaac
#   @desc:      These methods handle parsing data
#               
#****************************************************************************
class ParsingMethods():
	LAT_REGEX = re.compile(r"^Latitude: ([a-zA-Z0-9. -])*\r$")
	LNG_REGEX = re.compile(r"^Longitude: ([a-zA-Z0-9. -])*\r$")
		
	def parseGPSString(output):
		lines = output.split("\n")
		#get lat and long lines
		lat_dms = None
		lng_dms = None
		for line in lines:
			if LAT_REGEX.match(line):
				lat_dms = line
				break
				
		for line in lines:
			if LNG_REGEX.match(line):
				lng_dms = line
				break
				
		if not lat_dms and lng_dms:
			return
		
		#convert to doubles
		lat = convertLat(lat_dms)
		lng = convertLng(lng_dms)
		print lat
		print lng
		if not lat and lng:
			return None
		return lat, lng
				
	#convert lat_dms to degrees
	def convertLat(lat):
		lat_s = lat.split(" ")
		#bearing
		bearing = lat_s[-1:][0]
		bearing_val = None
		if bearing == 'North\r':
			bearing_val = 0
		else: #bearing is South
			bearing_val = 1
			
		#degrees
		lat_str = lat_s[1:-1]
		lat_nums = [lat_str[0], lat_str[2], lat_str[4]]
		#print 'Nums:'
		#print lat_nums
		secs = float(lat_nums[2]) / 3600
		#print secs
		mins = float(lat_nums[1]) / 60
		#print mins
		degs = float(lat_nums[0])
		#print degs
		lat_val = degs + mins + secs
		#print lat_val
		lat_val = float(format(lat_val, '.8f'))
		#print 'rounded:'
		#print lat_val
		if bearing_val is 1:
			return lat_val * -1
		return lat_val
		
	def convertLng(lng):
		lng_s = lng.split(" ")
		
		#bearing
		bearing = lng_s[-1:][0]
		bearing_val = None
		if bearing == 'West\r':
			bearing_val = 1
		else: #bearing is East
			bearing_val = 0
			
		#degrees
		lng_str = lng_s[1:-1]
		lng_nums = [lng_str[0], lng_str[2], lng_str[4]]
		#print 'Nums:'
		#print lng_nums
		secs = float(lng_nums[2]) / 3600
		#print secs
		mins = float(lng_nums[1]) / 60
		#print mins
		degs = float(lng_nums[0])
		#print degs
		lng_val = degs + mins + secs
		#print lng_val
		lng_val = float(format(lng_val, '.8f'))
		#print 'rounded:'
		#print lng_val
		if bearing_val is 1:
			return lng_val * -1
		return lng_val