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

GMAPS_API_KEY = "AIzaSyBGqlkhPlQHdebR5LojhHwo4mdhr0hZUfQ"

flask_app = Flask('flaskapp')

@flask_app.route('/')
def index():
    return redirect('http://localhost:8095/liveview')

@flask_app.route('/liveview', methods=['GET'])
def liveview():
    updateGPSCoords()
    markers = json.dumps(getMarkers(), indent=2)
    if markers:
        return render_template('mapscripts.html', markers=markers, api_key=GMAPS_API_KEY), 200
    return render_template('mapscripts.html', api_key=GMAPS_API_KEY), 200

@flask_app.route('/_query_db')
def query_db():
	updateGPSCoords()
	markers = json.dumps(getMarkers(), indent=2)
	if markers:
		return markers
	return None

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect('http://localhost:8095/liveview')

#DB methods
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

def updateGPSCoords():
	DB = connect()
	c = DB.cursor()
	query = "SELECT * FROM UserAgent"
	c.execute(query)
	rows = c.fetchall()
	for user in rows:
		print user
		print user[1]
		getGPSCoords(user[1])
    #query = "UPDATE Marker SET latitude = %s, longitude = %s WHERE id = %s" % (lat,lng,id)
    #c.execute(query)
    #DB.commit()
	DB.close()

#Remote data fetching methods
def getGPSCoords(username):
	DB = connect()
	c = DB.cursor()
	query = "SELECT * FROM UserAgent WHERE username=(%s)"
	c.execute(query, (username,))
	user = c.fetchone()
	DB.close()
	
	# Access variables.
	hostname = user[3]
	port = 22
	username = user[1]
	password = user[2]
	sudo_password = password  # assume that it is the same password
	
	ssh = MySSH()
	ssh.connect(hostname, username, password)
	status, output = ssh.run('enable')
	print 'status = %d' % (status)
	print 'output (%d):' % (len(output))
	print '%s' % (output)

app = flask_app.wsgi_app