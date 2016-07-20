#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ FLASKAPP.PY ~
#   @author:    james macisaac
#   @created:   May 20th, 2016
#   @updated:   July 2016
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

import json
import paramiko # ssh library
import sys
import re

#REMOTE_EXEC.PY
from remote_exec import MySSH

#TIMEOUT.PY
from timeout import TimeoutError

#AUTHENTICATION.PY
from authentication import UserMethods
from authentication import Security

#DATABASE.PY
from database import DBMethods

#SSH.PY
from ssh import SSHMethods

#COMPUTE.PY
from compute import ParsingMethods

#****************************************************************************
#   GLOBALS
#   @author:    james macisaac
#   @desc:      a handy location to group all necessary globals so
#               that they can be easily altered
#****************************************************************************

GMAPS_API_KEY = "AIzaSyBGqlkhPlQHdebR5LojhHwo4mdhr0hZUfQ"

flask_app = Flask(__name__)
UserMethods.login_manager.init_app(flask_app)
#****************************************************************************
#   ROUTES
#   @author:    james macisaac
#   @desc:      These are the web app routing methods. Each maps a function 
#               to handle different route requests from a browser.
#****************************************************************************

@flask_app.route('/')
def index():
	return redirect('http://192.168.99.183:8095/login')

@flask_app.route('/liveview', methods=['GET'])
def liveview():
	print 'LiveView Requested'
	markers_raw = DBMethods.getMarkers()
	if markers_raw:
		markers = json.dumps(DBMethods.getMarkers(), indent=2)
	else:
		markers = markers_raw
	print markers
	if markers is None:
		return render_template('mapscripts.html', markers=None, api_key=GMAPS_API_KEY), 200
	return render_template('mapscripts.html', markers=markers, api_key=GMAPS_API_KEY), 200

@flask_app.route('/login', methods = ['GET', 'POST'])
def login():
	#check if they are logged in.
	if request.method == 'POST':
		return redirect('http://192.168.99.183:8095/liveview')
		#check the credentials safely here
	else: # GET
		return render_template('login.html'), 200
	
@flask_app.route('/_query_db')
def query_db():
	updateDatabase()
	markers = json.dumps(DBMethods.getMarkers(), indent=2)
	if markers:
		return markers
	return None

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect('http://192.168.99.183:8095/login')
	
app = flask_app.wsgi_app

#****************************************************************************
#   WRAPPERS
#   @author:    james macisaac
#   @desc:      Wrapper functions for the various areas of the application
#****************************************************************************

#***DATABASE*****************************************************************
def updateDatabase():
	agent_IDs = DBMethods.getAllAgentsID()
	print 'Updating DB'
	for agent in agent_IDs:
		SSHMethods.updateGPSCoords(agent[0])
	