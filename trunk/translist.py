#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Wang Yuanyi
'''
from decimal import Decimal
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, template
from google.appengine.ext.webapp.util import run_wsgi_app
from wiwikai import get_next_month_first_day
from wiwikai.faccbk import TransItem, TransAccount
from wiwikai.gae.template import get_template_file, utils
import datetime

class BaseTransListHandler(webapp.RequestHandler):
    def get_trans_item_list(self, start_time, end_time):
        return TransItem.gql("WHERE trans_date >= :q_start_time "
                                        "AND trans_date < :q_end_time "
                                        "ORDER BY trans_date",
                                        q_start_time = start_time,
                                        q_end_time = end_time )

    def get_trans_item_list_by_account(self, start_time, end_time, trans_account):
        return TransItem.gql("WHERE trans_account = :q_trans_account "
                                        "AND trans_date >= :q_start_time "
                                        "AND trans_date < :q_end_time "
                                        "ORDER BY trans_date",
                                        q_trans_account = trans_account.key(),
                                        q_start_time = start_time,
                                        q_end_time = end_time )
         
class MonthlyTransListHandler(BaseTransListHandler):
        
    def get(self, year, month):
        template_get = get_template_file('trans_list')
        template_values = {}
        
        int_year, int_month = int(year), int(month)

        time_scope_start = datetime.datetime(int_year, int_month, 1)
        time_scope_end = get_next_month_first_day(time_scope_start)
        
#        trans_item_list = super(MonthlyTransListHandler, self).get_trans_item_list( time_scope_start, time_scope_end )
        
#        template_values['trans_item_list'] = trans_item_list
        trans_list_month =  datetime.date(int_year, int_month, 1)
        template_values['bill_month'] = trans_list_month
        
#        template_values['trans_purpose_category_list'] = TransPurposeCategory.all()
        
        trans_account_list = TransAccount.all()
#        template_values['trans_account_list'] = TransAccount.all()
        
        trans_account_and_trans_list_list = []
        
        all_account_balance = Decimal(0);
        for trans_account in trans_account_list:
            all_account_balance += Decimal(trans_account.balance)
            
            trans_list = super(MonthlyTransListHandler, self).get_trans_item_list_by_account(time_scope_start, time_scope_end, trans_account)
            trans_account_and_trans_list = {'trans_account': trans_account, 'trans_list': trans_list}
            trans_account_and_trans_list_list.append(trans_account_and_trans_list)
            
        template_values['trans_account_and_trans_list_list'] = trans_account_and_trans_list_list
        template_values['all_account_balance'] = all_account_balance
        
#        template_values['previous_month'] = 
#        template_values['next_month'] = 
        
        self.response.out.write(utils.render(self.request, self.response, template_get, template_values))

class CurrentlyMonthlyTransListHandler(MonthlyTransListHandler):
    def get(self):
        now = datetime.datetime.now()
        return super(CurrentlyMonthlyTransListHandler, self).get(now.year, now.month)
        
#class AnnualTransListHandler(BaseTransListHandler):
#    def get(self, year):
#        now = datetime.datetime.now()
#        start_time = datetime.datetime(now.year, 1, 1)
#        end_time = datetime.datetime(now.year + 1, 1, 1)
#        return super(AnnualTransListHandler, self).get_trans_item_list(start_time, end_time)
    
application = webapp.WSGIApplication([
                                      ('/trans_list', CurrentlyMonthlyTransListHandler),
#                                      ('/trans_list/([1-9][0-9]{3})', AnnualTransListHandler),
                                      ('/trans_list/([1-9][0-9]{3})/([0-1][0-9])', MonthlyTransListHandler),
                                      ], debug=True)

def main():
    run_wsgi_app(application)


template.register_template_library('wiwikai.templatefilters.customfilters')


if __name__ == "__main__":
    main()
        