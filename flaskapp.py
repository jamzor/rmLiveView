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

from flask import (
Flask,
Response,
abort,
flash,
request,
render_template,
redirect,
url_for,
)

import json
import paramiko # ssh library
import sys
import re

from os import environ

#STORMPATH
from flask_stormpath import (
StormpathManager,
StormpathError,
User,
login_required,
login_user,
logout_user,
user,
)

#REMOTE_EXEC.PY
from remote_exec import MySSH

#TIMEOUT.PY
from timeout import TimeoutError

#AUTHENTICATION.PY
from authentication import (
MasterGeneration,
UserMethods,
Security,
)

#DATABASE.PY
from database import DBMethods

#SSH.PY
from ssh import SSHMethods

#COMPUTE.PY
from compute import ParsingMethods

#CONFIG FOLDER
from config.app_config import URL
from config.validation_config import (
USER_RE,
PASS_RE,
)
from config.gmaps_config import GMAPS_API_KEY

#****************************************************************************
#   STORMPATH CONFIGURATIONS
#   @author:    james macisaac
#   @desc:      All Stormpath configuration variables are found here.
#
#****************************************************************************

flask_app = Flask(__name__)

flask_app.config['SECRET_KEY'] = ']~x;hG!W*mPK#Tv6<P!g'
flask_app.config['STORMPATH_API_KEY_FILE'] = '~/.stormpath/apiKey.properties'
flask_app.config['STORMPATH_APPLICATION'] = 'LiveView'

flask_app.config['STORMPATH_REGISTRATION_REDIRECT_URL'] = URL + '/liveview'
flask_app.config['STORMPATH_REDIRECT_URL'] = URL + '/liveview' #basic redirect

flask_app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
flask_app.config['STORMPATH_ENABLE_USERNAME'] = True
flask_app.config['STORMPATH_REQUIRE_USERNAME'] = True

flask_app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True

stormpath_manager = StormpathManager(flask_app)

#directory = stormpath_manager.application.default_account_store_mapping.account_store

#masters = directory.groups.create({'name': 'Masters'})
#clients = directory.groups.create({'name': 'Clients'})

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
@login_required
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
		try:
			_user = User.from_login(
				request.form['username'],
				request.form['password'],
			)
			_user.add_group(masters)
			login_user(_user, remember=True)
			
		except StormpathError, err:
			print err.message
			return render_template('login.html', exist_error = 'Invalid Credentials')
	
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
@login_required
def master():
	cookie = getSecureCookie('sess_id')
	if cookie:
		# check if user has privileges
		return render_template('masterlanding.html'), 200
	else:
		return redirect(URL + '/login')
	
@flask_app.route('/_query_db')
@login_required
def query_db():
	updateDatabase()
	markers = json.dumps(DBMethods.getMarkers(), indent=2)
	if markers:
		return markers
	return None
	
@flask_app.route('/_logout')
@login_required
def logout():
	logout_user()
	# clear cookies
	#setSecureCookie(response, 'sess_id', '')
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
	