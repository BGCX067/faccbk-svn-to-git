#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from wiwikai import DecimalProperty
import datetime

trans_type_income = 'income'
trans_type_expense = 'expense'

trans_type_set = set([trans_type_income, trans_type_expense])

#trans_trading_card = 'card'
#trans_trading_cash = 'cash'

trans_account_type_credit_card = 'Credit Card'
trans_account_type_cash = 'Cash'
trans_account_type_debit_card = 'Debit Card'

trans_account_type_set = set ([trans_account_type_credit_card, trans_account_type_cash, trans_account_type_debit_card]) 

role_admin = 'administrator'
role_user  = 'user'

class UserPrefs(db.Model):
    user = db.UserProperty(required=True)
    role = db.StringListProperty(required=True)

class TransPurposeCategory(db.Model):
    title       = db.StringProperty(required=True)
    trans_type  = db.StringProperty(required=True, choices=trans_type_set)

class Payee(db.Model):
    title = db.StringProperty(required=True)

class TransAccount(db.Model):
    type                = db.StringProperty(required=True, choices=trans_account_type_set)
    last4number         = db.StringProperty(indexed=True)
    bank_name           = db.StringProperty(required=True)
    statement_date      = db.IntegerProperty(required=True)
    payment_due_date    = db.IntegerProperty(required=True)
    balance             = DecimalProperty(default='0.00')
    initial_value       = DecimalProperty(default='0.00')
    disable_flag        = db.BooleanProperty(default=False)

class TransItem(db.Model):
    trans_account           = db.ReferenceProperty(TransAccount, required=True)
    information             = db.StringProperty()
    payee                   = db.ReferenceProperty(Payee)
    trans_purpose_category  = db.ReferenceProperty(TransPurposeCategory)
    
    trans_type              = db.StringProperty(required=True, choices=trans_type_set)
    description             = db.StringProperty()
    amount                  = DecimalProperty(required=True)
    
    internal_transfer_flag  = db.BooleanProperty(default=False)
#    transfer_to_account     = db.ReferenceProperty(TransAccount)
    
    trans_date              = db.DateProperty(required=True)
    post_time               = db.DateTimeProperty(auto_now_add=True)
    last_updated            = db.DateTimeProperty(auto_now=True)
    validate_flag           = db.BooleanProperty(default=False)

class InternalTransferLog(db.Model):
    trans_item_source = db.StringProperty(required=True)
    trans_item_target = db.StringProperty(required=True)
    
