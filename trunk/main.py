#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Yuanyi Wang
'''
from google.appengine.api import oauth, users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from wiwikai.gae.template import utils, get_template_file
import datetime
import os

openIdProviders = (
    'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
    'Yahoo.com',
    'MySpace.com',
    'AOL.com',
    'MyOpenID.com',
    # add more here
)

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            now = datetime.datetime.now()
            self.redirect('/trans_list/%d/%02d' % (now.year, now.month))
#            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
#                user.nickname(), users.create_logout_url(self.request.uri)))
        else:     # let user choose authenticator
            self.response.out.write('Hello world! Sign in at: ')
            for p in openIdProviders:
                p_name = p.split('.')[0] # take "AOL" from "AOL.com"
                p_url = p.lower()        # "AOL.com" -> "aol.com"
                self.response.out.write('[<a href="%s">%s</a>]' % (users.create_login_url(federated_identity=p_url), p_name))

class AboutHandler(webapp.RequestHandler):
    def get(self):
        s = ''
        for name in os.environ.keys():
            s = s +"%s = %s<br />\n" % (name, os.environ[name])
        
        template_values = {}
        template_values['OS_ENVIRONMENT'] = s
        template_get = get_template_file('about')
        self.response.out.write(utils.render(self.request, self.response, template_get, template_values))
        

application = webapp.WSGIApplication([
                                      ('/', MainHandler),
                                      ('/about', AboutHandler),
                                      ], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()