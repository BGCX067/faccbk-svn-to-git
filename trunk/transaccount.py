#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Wang Yuanyi
'''

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from wiwikai.gae.template import get_template_file
from wiwikai.faccbk import TransAccount

class TransAccountListHandler(webapp.RequestHandler):
    pass
class TransAccountHandler(webapp.RequestHandler):

    def get(self):
        """ get all visable accounts """
        template_values = {}
        
        trans_account_id = self.request.get('trans_account_id')
        
        if trans_account_id == '':
            trans_account_list = TransAccount.all()
            #.filter('disable_flag=', False)
            template_values['trans_account_list'] = trans_account_list
            template_get = get_template_file('trans_account_list')
            self.response.out.write(template.render(template_get, template_values))
        else:
            trans_account = TransAccount.get_by_id(trans_account_id)
            template_values['trans_accout'] = trans_account
            template_get = get_template_file('bill')
            self.response.out.write(template.render(template_get, template_values))
            
    def put(self):
        """ create a new account """
        trans_account = TransAccount()
        self._set_trans_account(self, trans_account)
        trans_account.put()
    
    def post(self):
        """ update account information """
        trans_account_id = self.request.get('trans_account_id')
        trans_account = TransAccount.get_by_id(trans_account_id)
        
        if trans_account is None:
            self.response.set_status(404)
        else:
            self._set_trans_account(self, trans_account)
            trans_account.put()
    
    def delete(self):
        """ set this account as disable """
        trans_account_id = self.request.get('trans_account_id')
        trans_account = TransAccount.get_by_id(trans_account_id)
        
        if trans_account is None:
            self.response.set_status(404)
        else:
            trans_account.index(0).disable_flag = True
            trans_account.index(0).put()
            
    def _set_trans_account(self, trans_account):
        trans_account.type = self.request.get('type')
        trans_account.number = self.request.get('number')
        trans_account.bank_name = self.request.get('bank_name')
        trans_account.statement_date = self.request.get('statement_date')
        trans_account.payment_due_date = self.request.get('payment_due_date')
        trans_account.balance = self.request.get('account_balance')
        #trans_account.initial_value = self.request.get('initial_value')
    
application = webapp.WSGIApplication([('/trans_account', TransAccountListHandler),
                                      ('/trans_account/\d', TransAccountHandler),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
        