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
                               (r'/*', RedirHandler)
                              ], debug = DEBUG)