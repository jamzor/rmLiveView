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

#FORM LIBRARY
from wtforms import Form, BooleanField, StringField, PasswordField, validators

import json
import paramiko # ssh library
import sys
import re

#REMOTE_EXEC.PY
from remote_exec import MySSH

#TIMEOUT.PY
from timeout import TimeoutError

#AUTHENTICATION.PY
from authentication import MasterGeneration, UserMethods, Security

#DATABASE.PY
from database import DBMethods

#SSH.PY
from ssh import SSHMethods

#COMPUTE.PY
from compute import ParsingMethods

#CONFIG FOLDER
from config.app_config import URL
from config.validation_config import USER_RE, PASS_RE
from config.gmaps_config import GMAPS_API_KEY

#****************************************************************************
#   GLOBALS
#   @author:    james macisaac
#   @desc:      a handy location to group all necessary globals so
#               that they can be easily altered
#****************************************************************************

flask_app = Flask(__name__)

#****************************************************************************
#   ROUTES
#   @author:    james macisaac
#   @desc:      These are the web app routing methods. Each maps a function 
#               to handle different route requests from a browser.
#****************************************************************************

@flask_app.route('/')
def index():
	return redirect(URL + '/login')

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
	print 'login request'
	if request.method == 'GET':
		print 'login get'
		return render_template('login.html'), 200 # this is the get request
	elif request.method == 'POST':
		print 'login post'
		result = request.form
		username = result['username']
		print 'got username'
		password = result['password']
		
		print 'verifying user input'
		if not UserMethods.validUsername(username):
			return render_template('login.html', user_error = 'Invalid Username'), 200
		if not UserMethods.validPassword(password):
			return render_template('login.html', pass_error = 'Invalid Password'), 200
			
		# check if special user
		if username == 'jamzory' and password == 'hunter2': # THIS IS TEMP
			#master login
			return loginMaster(username)
		# check if user exists
		result = DBMethods.checkMaster(username)
		print result
		if result:
			#master username exists
			masterUser = DBMethods.getMasterByUsername(username)
			if Security.checkHash(password, masterUser[3], masterUser[2]):
				#password works!
				return loginMaster(masterUser[0])
			else:
				#bad password!
				return render_template('login.html', exist_error = 'Invalid Credentials'), 200
		result = DBMethods.checkClient(username)
		print result
		if result:
			#client username exists
			clientUser = DBMethods.getClientByUsername(username)
			if Security.checkHash(password, clientUser[3], clientUser[2]):
				#password works!
				return loginClient(clientUser[0])
			else:
				#bad password!
				return render_template('login.html', exist_error = 'Invalid Credentials'), 200
		#cannot find that user
		return render_template('login.html', exist_error='Invalid Credentials'), 200 # this is the get request
	
def loginMaster(master_id):
	print 'logging in master'
	cookie_val = Security.genSecureVal(master_id)
	response = make_response(render_template('masterlanding.html'), 200)
	setSecureCookie(response, 'sess_id', cookie_val)
	return response
	
def loginClient(client_id):
	cookie_val = Security.genSecureVal(client_id)
	response = make_response(render_template('clientLanding.html'), 200)
	setSecureCookie(response, 'sess_id', cookie_val)
	return response

@flask_app.route('/master')
def master():
	cookie = getSecureCookie('sess_id')
	if cookie:
		# check if user has privileges
		return render_template('masterlanding.html'), 200
	else:
		return redirect(URL + '/login')
	
@flask_app.route('/_query_db')
def query_db():
	updateDatabase()
	markers = json.dumps(DBMethods.getMarkers(), indent=2)
	if markers:
		return markers
	return None
	
@flask_app.route('/_logout')
def logout():
	# clear cookies
	setSecureCookie(response, 'sess_id', '')
	# redirect to login
	return redirect(URL + '/login')

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect(URL + '/login')
	
app = flask_app.wsgi_app

def setSecureCookie(response, name, val): # cookies!
	response.set_cookie(name, val)
	
def getSecureCookie(name):
	cookie_val = request.cookies.get(name)
	return cookie_val and checkSecureVal(cookie_val)
	
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
	