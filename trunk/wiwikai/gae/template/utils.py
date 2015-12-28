#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Wang Yuanyi
'''

from google.appengine.api import users
from google.appengine.ext import webapp
from wiwikai.gae.template import get_template_file
import config
import os

def render(request, response, template_path, template_values):
    current_user = users.get_current_user()
    
    if (current_user is None) or not (current_user.email() in config.Users):
        response.set_status(403)
        template_path = get_template_file('errors/503')
        return webapp.template.render(template_path, None)
    
    template_values['user'] = current_user
    template_values['logout_url'] = users.CreateLogoutURL(request.uri)
    template_values['admin_flag'] = (current_user.email() == config.Admin)
    template_values['development_flag'] = config.DEVELOPMENT
    template_values['CURRENT_VERSION_ID'] = os.environ['CURRENT_VERSION_ID']
    template_values['producation_env_admin_url'] = 'https://appengine.google.com/dashboard?&app_id=' + os.environ['APPLICATION_ID']
    
    return webapp.template.render(template_path, template_values)