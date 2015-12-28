#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''''
@author: Wang Yuanyi
'''
from datetime import datetime, date
from decimal import Decimal
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from wiwikai.gae.template import get_template_file
from wiwikai.faccbk import TransItem, TransPurposeCategory, TransAccount, \
    trans_type_income, Payee
from wiwikai.gae.template import utils

def set_basic_data(template_values):
    template_values['trans_purpose_category_list'] = TransPurposeCategory.all()
    template_values['trans_account_list'] = TransAccount.all()
    template_values['payee_list'] = Payee.all()

def handle_amount(amount, trans_type):
    if trans_type_income == trans_type:
        return (0 - amount, amount)[amount > 0]
    else:
        return (0 - amount, amount)[amount < 0]

class TransHandler(webapp.RequestHandler):
    def get(self):
        template_get = get_template_file('new_trans')
        template_values = {}
        
        set_basic_data(template_values)
        
        self.response.out.write(utils.render(self.request, self.response, template_get, template_values))
    
    def post(self):
        """ Create new transaction item """
        p_trans_account = self.request.get('trans_account')
        p_trans_purpose_category = self.request.get('trans_purpose_category')
        p_information = self.request.get('information')
        p_payee = self.request.get('payee')
        p_trans_type = self.request.get('trans_type')
        p_description = self.request.get('description')
        p_amount = Decimal(self.request.get('amount'))
        p_trans_date1 = datetime.strptime(self.request.get('trans_date'), '%Y-%m-%d')
        p_trans_date = date(p_trans_date1.year, p_trans_date1.month, p_trans_date1.day)

        trans_account = TransAccount.get(p_trans_account)
        trans_purpose_category = TransPurposeCategory.get(p_trans_purpose_category)
        payee = Payee.get(p_payee)
        
        p_amount = handle_amount(p_amount, p_trans_type)
        
        trans = TransItem(parent=None, trans_account = trans_account,
                          trans_purpose_category = trans_purpose_category,
                          information = p_information,
                          payee = payee,
                          trans_type = p_trans_type,
                          description = p_description,
                          amount = p_amount,
                          trans_date = p_trans_date)
        
        trans_account.balance = trans_account.balance + trans.amount

        trans_account.put()
        trans.put()

        self.redirect('/trans_list')
        
class UpdateTransHandler(webapp.RequestHandler):
    def get(self, key):
        template_get = get_template_file('new_trans')
        template_values = {}
        
        trans = TransItem.get(key)
        
        if trans is None:
            self.response.set_status(404)
            return
        
        set_basic_data(template_values)
        
        template_values['transaction'] = trans
        template_values['transaction_update_flag'] = True
        template_values['transaction_key'] = key
        
        self.response.out.write(utils.render(self.request, self.response,template_get, template_values))
        
    def post(self, key):
        """update transaction"""
        trans = TransItem.get(key)
        
        if trans is None:
            self.response.set_status(404)
            return
        
        p_trans_account = self.request.get('trans_account')
        p_trans_purpose_category = self.request.get('trans_purpose_category')
        p_payee = self.request.get('payee')
        
        
        p_amount = Decimal(self.request.get('amount'))
        trans_account = TransAccount.get(p_trans_account)
        
        p_trans_date1 = datetime.strptime(self.request.get('trans_date'), '%Y-%m-%d')
        trans.trans_date = date(p_trans_date1.year, p_trans_date1.month, p_trans_date1.day)
        
        trans.trans_account = trans_account
        trans.trans_purpose_category = TransPurposeCategory.get(p_trans_purpose_category)
        trans.payee = Payee.get(p_payee)
        
        trans.information = self.request.get('information')
        trans.trans_type = self.request.get('trans_type')
        trans.description = self.request.get('description')
        
        trans_account.balance = trans_account.balance - trans.amount
        
        trans.amount = handle_amount(p_amount, trans.trans_type)
        
        trans_account.balance = trans_account.balance + trans.amount

        trans_account.put()
        trans.put()

        self.redirect('/trans_list')
        
application = webapp.WSGIApplication([
                                      ('/trans', TransHandler),
                                      ('/trans/(\w+)', UpdateTransHandler)
                                      ], debug=True)

def main():
    run_wsgi_app(application)

template.register_template_library('wiwikai.templatefilters.customfilters')

if __name__ == "__main__":
    main()
