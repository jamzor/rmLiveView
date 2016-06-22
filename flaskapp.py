#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ FLASKAPP.PY ~
#   @author:    james macisaac
#   @created:   May 20th, 2016
#   @updated:   June 2016
#   @project:   Live View
#   @desc:      This file contains the logic behind the Flask application for
#               LiveView. Uses remote_exec as a helper class.
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect, url_for

import psycopg2
from psycopg2.extras import RealDictCursor
import json

import paramiko # ssh library
import sys
from remote_exec import MySSH

import re

#****************************************************************************
#   GLOBALS
#   @author:    james macisaac
#   @desc:      a handy location to group all necessary regular expressions so
#               that they can be easily altered
#****************************************************************************

GMAPS_API_KEY = "AIzaSyBGqlkhPlQHdebR5LojhHwo4mdhr0hZUfQ"

LAT_REGEX = re.compile(r"^Latitude: ([a-zA-Z0-9. -])*\r$")
LNG_REGEX = re.compile(r"^Longitude: ([a-zA-Z0-9. -])*\r$")

flask_app = Flask('flaskapp')

#****************************************************************************
#   ROUTES
#   @author:    james macisaac
#   @desc:      These are the web app routing methods. Each maps a function 
#               to handle different route requests from a browser.
#****************************************************************************

@flask_app.route('/')
def index():
    return redirect('http://localhost:8095/liveview')

@flask_app.route('/liveview', methods=['GET'])
def liveview():
    updateDatabase()
    markers = json.dumps(getMarkers(), indent=2)
    if markers:
        return render_template('mapscripts.html', markers=markers, api_key=GMAPS_API_KEY), 200
    return render_template('mapscripts.html', api_key=GMAPS_API_KEY), 200

@flask_app.route('/_query_db')
def query_db():
	updateDatabase()
	markers = json.dumps(getMarkers(), indent=2)
	if markers:
		return markers
	return None

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect('http://localhost:8095/liveview')

#****************************************************************************
#   DB METHODS
#   @author:    james macisaac
#   @desc:      These are all of the Database methods to handle common 
#               database operations for the program.
#****************************************************************************
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=liveview")

def getMarkers():
    """Get the list of markers from the database"""
    DB = connect()
    c = DB.cursor(cursor_factory=RealDictCursor)
    query = "SELECT id,name,latitude,longitude,link FROM Marker ORDER BY created DESC"
    c.execute(query)
    rows = c.fetchall()
    DB.close()
    return rows

def updateDatabase():
	DB = connect()
	c = DB.cursor()
	query = "SELECT * FROM UserAgent"
	c.execute(query)
	rows = c.fetchall()
	DB.close()
	for user in rows:
		updateGPSCoords(user[1])
	
#****************************************************************************
#   SSH METHODS
#   @author:    james macisaac
#   @desc:      This block holds the SSH related Methods. It handes opening 
#               the connection amongst other things.
#****************************************************************************

def updateGPSCoords(name):
	DB = connect()
	c = DB.cursor()
	query = "SELECT * FROM UserAgent WHERE username=(%s)"
	c.execute(query, (name,))
	user = c.fetchone()
	DB.close()
	
	if not user:
		return
	
	#run commands on ssh
	ssh = openSSHSession(user)
	ssh.run('enable')
	ssh = openSSHSession(user)
	status, output = ssh.run('show cellular 0 gps')
	
	#print 'status = %d' % (status)
	#print 'output (%d):' % (len(output))
	#print '%s' % (output)
	
	#parse the response
	lat, lng = parseGPSString(output)
	
	#update DB
	DB = connect()
	c = DB.cursor()
	query = "UPDATE Marker SET latitude = %s, longitude = %s, updated = CURRENT_TIMESTAMP WHERE name = %s"
	c.execute(query, (lat,lng,name,))
	DB.commit()
	DB.close()
	
def openSSHSession(user):
	# Access variables.
	hostname = user[3]
	port = 22
	username = user[1]
	password = user[2]
	sudo_password = password  # assume that it is the same password
	
	ssh = MySSH()
	ssh.connect(hostname, username, password)
	return ssh
	
#****************************************************************************
#   DATA PARSING
#   @author:    james macisaac
#   @desc:      These methods handle parsing the Router GPS response and 
#               making sense of the text that is given back
#****************************************************************************
	
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
	lng = convertLat(lng_dms)
	
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
	secs = float(lat_nums[2]) / 3600
	mins = int(lat_nums[1]) / 60
	degs = int(lat_nums[0])
	lat_val = degs + mins + secs
	
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
	secs = float(lng_nums[2]) / 3600
	mins = float(lng_nums[1]) / 60
	degs = float(lng_nums[0])
	lng_val = degs + mins + secs
	
	if bearing_val is 1:
		return lng_val * -1
	return lng_val
	
app = flask_app.wsgi_app