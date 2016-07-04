#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ SSH.PY ~
#   @author:    james macisaac
#   @created:   July 4th, 2016
#   @updated:   July 2016
#   @project:   Live View
#   @desc:      This file Handles the methods which invoke remote execution 
#               commands on an ssh session, and sets up said session.
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

import paramiko # ssh library

from database import DBMethods
from compute import ParsingMethods

#****************************************************************************
#   SSH METHODS
#   @author:    james macisaac
#   @desc:      This block holds the SSH related Methods. It handes opening 
#               the connection amongst other things.
#****************************************************************************
class SSHMethods():
	def updateGPSCoords(a_id):
		agent = DBMethods.getAgentByID(a_id)
		
		marker_IDs = DBMethods.getAgentMarkersID(a_id)
		for marker_ID in marker_IDs:
			agent_username = agent[1]
			agent_pw = agent[2]
			device_ID = DBMethods.getDeviceIDByMarkerID(marker_ID)
			device_addr = DBMethods.getDeviceAddrByID(device_ID)
			try:
				
				#run commands on ssh
				ssh = openSSHSession(agent_username, agent_pw, device_addr)
				if not ssh:
					return
				ssh.run('enable')
				ssh = openSSHSession(agent_username, agent_pw, device_addr)
				if not ssh:
					return
				status, output = ssh.run('show cellular 0 gps')
			except TimeoutError:
				return
			
			#print 'status = %d' % (status)
			#print 'output (%d):' % (len(output))
			#print '%s' % (output)
			
			#parse the response
			lat, lng = ParsingMethods.parseGPSString(output)
			
			#update DB
			DBMethods.updateMarker(lat,lng,m_id)
		
		
	def openSSHSession(agent_username, agent_pw, device_addr):
		# Access variables.
		hostname = device_addr
		port = 22
		username = agent_username
		password = agent_pw
		sudo_password = password  # assume that it is the same password

		ssh = MySSH()
		ssh.connect(hostname, username, password)
		return ssh