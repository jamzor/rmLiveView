
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ LIVEVIEW.PY ~
#   @author:    james macisaac
#   @created:   May 20th, 2016
#   @updated:   May 2016
#   @project:   Live View
#   @desc:      this file contains the main logic behind the liveview app.
#
#
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#****************************************************************************
#   IMPORTS
#   @author:    james macisaac
#   @desc:      import and file dependency declaration hub
#               central spot to make changes to libraries
#****************************************************************************

import os

import webapp2
import jinja2



from lib.utils import GOOGLE_MAPS_API_KEY

from lib.utils import Handler
from lib.utils import DEBUG

#****************************************************************************
#   CLASSES
#   @author:    james macisaac
#   @desc:      All of the classes with each page's logic lie here. Must add
#               some code to handler parsing a page and gathering data from
#               it.
#****************************************************************************

class DefaultPage(Handler):
    def get(self):
        self.render('mapscripts.html', api_key = GOOGLE_MAPS_API_KEY)

class LoginHandler(Handler):
    def get(self):
        self.render('login-form.html', next_url = next_url)
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid Login'
            self.render('login-form.html', error = msg)

class RedirHandler(Handler):
    def get(self):
        self.redirect('/')

#****************************************************************************
#   WEBAPP BINDING
#   @author:    james macisaac
#   @desc:      declares the url to class mappings for the application. This
#               dictates the structure of the app.
#****************************************************************************

app = webapp2.WSGIApplication([
                               ('/', DefaultPage),
                               ('/login', Login),
                               (r'/*', RedirHandler)
                              ], debug = DEBUG)