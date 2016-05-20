#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#   ~ UTILS.PY ~
#   @author:    james macisaac
#   @created:   May 20th, 2016
#   @updated:   May 2016
#   @project:   Live View
#   @desc:      this file contains utility functions for the various classes
#               it supports. Some managed by the Handler class, others are
#               floating.
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
import os.path
import re
import logging
import json

import webapp2
import jinja2

from google.appengine.api import memcache
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

DEBUG = bool(os.environ['SERVER_SOFTWARE'].startswith('Development'))
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)

#****************************************************************************
#   REGEXES
#   @author:    james macisaac
#   @desc:      a handy location to group all necessary regular expressions so
#               that they can be easily altered
#****************************************************************************

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")# letters, numbers, _ , - , size 3 < x < 20
PASS_RE = re.compile(r"^.{3,20}$")
PAGE_RE = re.compile(r"^(/(?:[a-zA-Z0-9_-]+/?)*)$") # letters, numbers, _ , -

#****************************************************************************
#   UTILITIES
#   @author:    james macisaac
#   @desc:      this file contains utility functions for the various classes
#               it supports. Some managed by the Handler class, others are
#               floating.
#****************************************************************************

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # allow content to be displayed as json for site queries
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    # set a secure cookie in the user's browser
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
                                         'Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    # read a secure cookie hash value
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val

    def notfound(self):
        self.error(404)
        self.write('<h1>404: Not Found</h1>We had some trouble finding that page...')