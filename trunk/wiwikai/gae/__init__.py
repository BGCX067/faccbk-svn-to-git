#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config

def _t(key):
    if config.LANGUAGE.has_key(key):
        return config.LANGUAGE[key]
    return key