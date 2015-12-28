#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Wang Yuanyi
'''

from google.appengine.ext.webapp import template
from wiwikai.gae import _t

register = template.create_template_register()

@register.filter(name='money')
def money(number):
#    return number
    if number == '':
        return ("%10.2f" % 0.0).lstrip()
    else:
        return ("%10.2f" % number).lstrip()

@register.filter(name='transtype2colorclass')
def transtype2colorclass(amount):
    if amount >= 0:
        return 'money_income'
    else:
        return 'money_expense'

@register.filter(name='get_account_name')
def get_account_name(account):
    return "[%s]-[%s]-[%s]" % (account.bank_name, _t(account.type), account.last4number)

@register.filter(name='compare0')
def compare0(number):
    return number >= 0

@register.filter(name='trans')
def trans(key):
    return _t(key)

