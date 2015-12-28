#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
import datetime
import decimal
import os

def get_next_month_first_day(time):
    month = time.month + 1
    year1 = 0
    
    if month > 12:
        month1 = 1
        year1 = 1
    else:
        month1 = month
    
    return datetime.datetime(time.year + year1, month1, 1)

def get_next_year_first_day(time):
    return datetime.datetime(time.year + 1, 1, 1)

class DecimalProperty(db.Property):
    data_type = decimal.Decimal

    def get_value_for_datastore(self, model_instance):
        return str(super(DecimalProperty, self).get_value_for_datastore(model_instance))

    def make_value_from_datastore(self, value):
        return decimal.Decimal(value)