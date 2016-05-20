import os

import webapp2
import jinja2

from lib.utils import Handler
from lib.utils import DEBUG

class DefaultPage(Handler):
    def get(self):
        self.render('base.html', text="Placeholder text.")

app = webapp2.WSGIApplication([
                              ('/', DefaultPage)
                              ], debug = DEBUG)