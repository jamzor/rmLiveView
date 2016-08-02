#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ DATABASE.PY ~
#   @author:    james macisaac
#   @created:   July 4th, 2016
#   @updated:   July 2016
#   @project:   Live View
#   @desc:      This file handles all of the direct database operations for 
#               the LiveView App.
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import ProgrammingError
from config.db_config import DATABASE_NAME
#****************************************************************************
#   DB METHODS
#   @author:    james macisaac
#   @desc:      These are all of the Database methods to handle common 
#               database operations for the program.
#****************************************************************************

class DBMethods():
	@classmethod
	def connect(self):
		"""Connect to the PostgreSQL database.  Returns a database connection."""
		return psycopg2.connect("dbname=%s" % DATABASE_NAME)
		
	#Query wrapper function
	@classmethod
	def runQuery(self, query, one, commit, *args):
		"""run a database query and return the response"""
		DB = self.connect()
		c = DB.cursor(cursor_factory=RealDictCursor)
		try:
			c.execute(query, args)
			if not commit:
				if one == True:
					response = c.fetchone()
				else:
					response = c.fetchall()
			else:
				response = None
				DB.commit()
			DB.close()
			return response
		except ProgrammingError:
			print "Query failed"
			return False
			
#***MASTERS AND CLIENTS********************************************************
	@classmethod
	def checkUsername(self, username):
		"""Check for the Username in the Tables"""
		query = "SELECT username FROM masters, clients WHERE username = (%s)"
		exists = runQuery(query, True, False, username)
		if exists:
			return False
		return True
		
	@classmethod
	def checkEmail(self, email):
		"""Check for the Email in the Tables"""
		query = "SELECT username FROM masters, clients WHERE email = (%s)"
		exists = runQuery(query, True, False, email)
		if exists:
			return False
		return True
		
#***MASTERS*******************************************************************
	@classmethod
	def addNewMaster(self, username, pw_hash, salt, email, enable):
		"""Add a new Master to the Database"""
		user_ok = checkUsername(username)
		if not user_ok:
			return False, 'Username in use'
		email_ok = checkEmail(email)
		if not email_ok:
			return False, 'Email already registered'
		query = "INSERT INTO masters (username, pw_salty, salt, email, enable) VALUES (%s, %s, %s, %s, %s)"
		runQuery(query, False, True, [username,pw_hash,salt,email,enable])
		return True, 'Success!'
		
	@classmethod
	def checkMaster(self, username):
		"""Check for the Username in the Masters Table"""
		query = "SELECT u_id FROM masters WHERE username = %s,enabled = 'True'"
		exists = runQuery(query, True, False, username)
		if exists:
			return exists[0]
		return False
		
	@classmethod
	def getMasterByUsername(self, username):
		query = "SELECT u_id,username,pw_salty,salt,email FROM masters WHERE username = %s"
		masterUser = runQuery(query, True, False, username)
		if masterUser:
			return masterUser
		return False
		
#***CLIENTS*******************************************************************
	@classmethod
	def getClientByID(self, id):
		"""Return the Client with the given ID"""
		query = "SELECT u_id,username,pw_salty,salt "

	@classmethod
	def checkClient(self, username):
		"""Check for the Username in the Masters Table"""
		query = "SELECT u_id FROM clients WHERE username = %s,enabled = 'True'"
		exists = runQuery(query, True, False, username)
		if exists:
			return exists[0]
		return False
		
	@classmethod
	def getClientByUsername(self, username):
		query = "SELECT u_id,username,pw_salty,salt,email FROM clients WHERE username = %s"
		clientUser = runQuery(query, True, False, username)
		if clientUser:
			return clientUser
		return False

#***COMPANIES*****************************************************************
	@classmethod
	def getCompanyID(self, company):
		"""Get the Company ID that matches this company name"""
		query = "SELECT c_id FROM Companies WHERE company_name = %s"
		comp_ID = runQuery(query, True, False, company)
		return comp_ID
	
#***AGENTS********************************************************************
	@classmethod
	def getAgentByID(self, a_id):
		"""Get The Agent that matches the given name"""
		query = "SELECT * FROM Agents WHERE a_id = %s"
		agent = runQuery(query, True, False, a_id)
		return agent
		
	@classmethod
	def getAllAgents(self):
		"""Get All Agents in the database"""
		query = "SELECT a_id,agent_name,pw,company_id FROM Agents"
		rows = runQuery(query, False, False, name)
		return rows
		
#***DEVICES*******************************************************************
	@classmethod
	def getDeviceAddrByID(self, d_id):
		query = "SELECT device_address FROM Devices WHERE d_id = (%s)"
		device_addr = runQuery(query, True, False, d_id)
		return device_addr
	
#***MARKERS*******************************************************************
	@classmethod
	def updateMarker(self, lat,lng,m_id):
		query = "UPDATE Marker SET latitude = %s, longitude = %s, updated = CURRENT_TIMESTAMP WHERE m_id = %s"
		runQuery(query, True, True, m_id)
		return
		
	@classmethod
	def getDeviceIDByMarkerID(self,m_id):
		query = "SELECT device_id FROM Marker WHERE m_id = (%s)"
		device_id = runQuery(query, True, False, m_id)
		return device_id
		
	@classmethod
	def getDeviceMarkerID(self,d_id):
		query = "SELECT m_id FROM Markers WHERE device_id = (%s)"
		marker_ID = runQuery(query, True, False, d_id)
		return marker_ID
		
	@classmethod
	def getMarkers(self):
		"""Get the list of markers from the database"""
		query = "SELECT m_id,title,latitude,longitude,device_address FROM Markers ORDER BY created DESC"
		rows = self.runQuery(query, False, False)
		return rows
		
	@classmethod
	def getAgentMarkersID(self,a_id):
		"""GET all the marker ids associated with the agent"""
		query = "SELECT m_id FROM Markers WHERE agent_id = (%s)"
		rows = runQuery(query, False, False)
		return rows
		
	@classmethod
	def getCompanyMarkers(self,company):
		"""Get the list of the company's markers from the database"""
		c_ID = getCompanyID(company)
		query = "SELECT m_id,title,latitude,longitude,device_address FROM Markers WHERE c_id = (%s) ORDER BY created DESC"
		rows = runQuery(query, False, False, c_ID)
		return rows