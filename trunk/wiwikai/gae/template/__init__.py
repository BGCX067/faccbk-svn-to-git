#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

template_folder = os.path.join(os.path.dirname(__file__), '../../..', 'templates')

def get_template_file(template_name):
    return os.path.join(template_folder, template_name + '.html')