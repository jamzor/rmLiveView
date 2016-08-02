#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ AUTHENTICATION.PY ~
#   @author:    james macisaac
#   @created:   July 4th, 2016
#   @updated:   July 2016
#   @project:   Live View
#   @desc:      This file holds the User account and authentication methods 
#               for the Liveview application.
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

from database import DBMethods

import hashlib
import binascii	#These are used to implement a PKCS#5 pw-based key der func
from base64 import b64encode
from os import urandom

#CONFIG FOLDER
from config.validation_config import USER_RE, PASS_RE
from config.security_config import SECRET_KEY

#****************************************************************************
#   USER GENERATION METHODS
#   @author:    james macisaac
#   @desc:      These methods handle the creation of user accounts.
#****************************************************************************

class MasterGeneration():
	@classmethod
	def createMasterAcc(self, username, pw, email, enable):
		# hash the password
		
		pw_hash, salt = Security.generateHash(pw) # calls the crypto methods
		
		result, status = DBMethods.addNewMaster(username, pw_hash, salt, email, True)
		print status
		if result:
			return True
		return False

#****************************************************************************
#   USER METHODS
#   @author:    james macisaac
#   @desc:      These methods handle user authentication and other related 
#               tasks in the app.
#****************************************************************************

class UserMethods():

	@classmethod
	def validUsername(self, username):
		return username and USER_RE.match(username)

	@classmethod
	def validPassword(self, password):
		return password and PASS_RE.match(password)
		
	#@classmethod
	#def userLogin(self, username, password):
		

#****************************************************************************
#   SECURITY
#   @author:    james macisaac
#   @desc:      These methods handle the data encryption and security side 
#               of things for the User accounts.
#****************************************************************************

HASH_ALGORITHM = 'sha256'
ROUNDS = 100000

class Security():
	@classmethod
	def genSalt():
		rgn = os.urandom(64)
		salt = b64encode(rgn).decode('utf-8') # 64 byte OS RGN salt for hash
		return salt

	@classmethod
	def generateHash(self, pw, salt=None):
		pass_enc = pw.encode()
		if salt:
			salt_enc = salt.encode()
		else:
			salt_enc = genSalt()
		hash = binascii.hexlify(hashlib.pbkdf2_hmac(HASH_ALGORITHM, pass_enc, salt_enc, ROUNDS))
		hash_dec = hash.decode()
		return hash_dec, salt_enc.decode()
		
	@classmethod
	def checkHash(self, pw, salt, hash):
		new_hash, new_salt = generateHash(pw,salt)
		if hash == new_hash:
			return True
		else:
			return False

	@classmethod
	def genSecureVal(self, val):
		return '%s|%s' % (val, hmac.new(SECRET_KEY, val).hexdigest())
		
	@classmethod
	def checkSecureVal(self, sec_val):
		val = secure_val.split('|')[0]
		if secure_val == genSecureVal(val):
			return val
		