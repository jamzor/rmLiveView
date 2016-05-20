import os

import webapp2
import jinja2

from lib.utils import GOOGLE_MAPS_API_KEY

from lib.utils import Handler
from lib.utils import DEBUG

class DefaultPage(Handler):
    def get(self):
        self.render('mapscripts.html', api_key = GOOGLE_MAPS_API_KEY)

class RedirHandler(Handler):
    def get(self):
        self.redirect('/')

app = webapp2.WSGIApplication([
                               ('/', DefaultPage),
                               (r'/*', RedirHandler)
                              ], debug = DEBUG)