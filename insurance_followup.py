# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class insurance_department(osv.osv):
    _description = "Insurance Department"
    _name = 'insurance.department'
    _columns = {
                'name': fields.char('Name', size=64, required=True),
                'code': fields.char('Code', size=64 ),
    }

insurance_department()


class insurance_payment(osv.osv):
    _description = "Insurance  Payment"
    _name = 'insurance.payment'
    _columns = {
                'paid_amt': fields.float('Paid Amount'),
                'date': fields.date('Date'),
                'payment_id': fields.many2one('insurance.followup','Payment')
    }
 
insurance_payment()
class insurance_followup(osv.osv):
	""" insurance_followup """
	_name = "insurance.followup"
	_description = "insurance followup"

	'''def _due_date(self, cr, uid, ids, field_name, arg, context=None):
		if context is None:
			context = {}
		if not ids:
			ids = self.search(cr, uid, [])
		res = {}.fromkeys(ids, 0.0)
		if not ids:
			return res
		cur_obj = self.browse(cr, uid, ids, context=context)
		iss_date = datetime.now()
		pay_freq = datetime.now()
		for field in cur_obj:
			if field.issue_date and field.payment_frequency:
				iss_date = datetime.strptime(field.issue_date, '%Y-%m-%d')
				pay_freq = field.payment_frequency.no
				freq = 12 / pay_freq
			cur_date = datetime.today()
			add_month = iss_date
			while add_month <= cur_date:
				if str(add_month).split(' ')[0] == str(cur_date).split(' ')[0]:
					break
				add_month = add_month + relativedelta(months=freq)
			res.update({field.id : str(add_month)})
		return res'''

	def _due_date(self, cr, uid, ids, field_name, arg, context=None):
		if context is None:
			context = {}
		if not ids:
			ids = self.search(cr, uid, [])
		res = {}.fromkeys(ids, 0.0)
		if not ids:
			return res
		cur_obj = self.browse(cr, uid, ids, context=context)
		iss_date = datetime.now()
		pay_freq = datetime.now()
		for field in cur_obj:
			if field.issue_date and field.payment_frequency:
				iss_date = datetime.strptime(field.issue_date, '%Y-%m-%d')
				pay_freq = field.payment_frequency
				freq = 12 / pay_freq
			cur_date = datetime.today()
			add_month = iss_date
			while add_month <= cur_date:
				if str(add_month).split(' ')[0] == str(cur_date).split(' ')[0]:
					break
				add_month = add_month + relativedelta(months=freq)
			res.update({field.id : str(add_month)})
		return res

	_columns = {
		'name': fields.char('Name', size=64, required=True, states={'paid':[('readonly',True)]},),
		'surname': fields.char('Surname', size=64, states={'paid':[('readonly',True)]},),
		'address_id': fields.char('Address', states={'paid':[('readonly',True)]},),
		'phone': fields.char('Phone', size=64, states={'paid':[('readonly',True)]},),
		'email': fields.char('Email', size=240, states={'paid':[('readonly',True)]},),
		'issue_date': fields.date('Issue Date', readonly=True, states={'draft':[('readonly',False)]}, select=True ),
		'date_due':fields.function(_due_date, type='date', string="Payment date", store=True),
		#'date_due': fields.date('Payment Date', readonly=True, states={'draft':[('readonly',False)]}, select=True ),
		'expiry_date': fields.date('CREDIT CARD EXPIRATION DATE', states={'paid':[('readonly',True)]},),
		'payment_frequency': fields.integer('FREQUENCY OF PAYMENT', states={'paid':[('readonly',True)]}),
		'sum_insured': fields.integer('SUM INSURED', states={'paid':[('readonly',True)]},),
		'no_of_policy': fields.integer('Number of Policy', states={'paid':[('readonly',True)]},),
		#'company_id': fields.many2one('res.company', 'Company', states={'paid':[('readonly',True)]},),
		'insurance_issuer_id': fields.many2one('insurance.issuer', 'Insurance Issuer', states={'paid':[('readonly',True)]},),
		'prime': fields.float('Prime', size=64, states={'paid':[('readonly',True)]},),
		'form': fields.char('Form', size=64, states={'paid':[('readonly',True)]},),
		'plan': fields.char('Plan', size=64, states={'paid':[('readonly',True)]},),
		'user_id': fields.many2one('res.users', 'Agent', states={'paid':[('readonly',True)]},),
		'partner_id': fields.many2one('res.partner', 'Customer', states={'paid':[('readonly',True)]}, required=True,),
		'department_id':fields.many2one('insurance.department', 'Insurance Department', states={'paid':[('readonly',True)]},),
		'amount': fields.float('Amount',required=True,),
		'state': fields.selection([
			('draft','Draft'),
			('open','Open'),
			('paid','Paid'),
			('cancel','Cancelled'),
			],'Status', select=True,),
		'notes': fields.text('Notes'),
		'policy_status':fields.boolean('Policy Status'),
		'divisiones': fields.char('DIVISIONES'),
        'payment_ids': fields.one2many('insurance.payment', 'payment_id', 'Insurance Payment'),
        'off_payment': fields.boolean('Off Payment?')
	
	}
	_defaults ={
		'state' : 'draft'
	}
		
	def check_date(self, cr, uid, ins_ids=None, context=None):
		ins_ids = self.search(cr, uid, [('state', 'in', ['draft','open','paid'])], context=context)

		for ins_obj in self.browse(cr, uid, ins_ids, context=context):
			if ins_obj.issue_date and ins_obj.payment_frequency:
				iss_date = datetime.strptime(ins_obj.issue_date, '%Y-%m-%d')
				pay_freq = ins_obj.payment_frequency
				freq = 12 / pay_freq
				cur_date = datetime.today()
				add_month = iss_date
				while add_month <= cur_date:
					if str(add_month).split(' ')[0] == str(cur_date).split(' ')[0]:
						break
					add_month = add_month + relativedelta(months=freq)
					if add_month < cur_date:
						add_month = add_month + relativedelta(months=freq)
						self.write(cr, uid, ins_ids, {'date_due':add_month}, context)
				vals = {}
				vals = {
					'name':ins_obj.name,
					'partner_phone':ins_obj.phone,
					'date':ins_obj.issue_date,
					'partner_id':ins_obj.partner_id.id or False,
					'user_id':ins_obj.user_id.id or False,
						   }
				for45 = cur_date + relativedelta(days=45)
				for15 = cur_date + relativedelta(days=15)
				for15 = str(for15).split(' ')[0]
				for45 = str(for45).split(' ')[0]
				print "15days",for15,'=',ins_obj.date_due
				if (for45 == ins_obj.date_due ) or (for15 == ins_obj.date_due):
					res = self.pool.get('crm.phonecall').create(cr, uid, vals, context=context)
		return True 
insurance_followup()
    
class insurance_followup_followup(osv.osv):
    _name = 'insurance_followup.followup'
    _description = 'Insurance Follow-up'
   # _rec_name = 'name'
    _columns = {
        'followup_line': fields.one2many('insurance_followup.followup.line', 'followup_id', 'Follow-up'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'name': fields.related('company_id', 'name', type='char', string = "Name"),
    }
    #_defaults = {
     #   'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'insurance_followup.followup', context=c),
    #}
    _sql_constraints = [('company_uniq', 'unique(company_id)', 'Only one follow-up per company is allowed')] 
    
insurance_followup_followup()

class payment_frequency(osv.osv):
    _name = 'payment.frequency'
    _rec_name = 'no'
    _columns = {
	'no': fields.char('Frequency', required=True),
	'desc': fields.char('Description'),
	}
payment_frequency()

class insurance_followup_followup_line(osv.osv):
    _name = 'insurance_followup.followup.line'
    _description = 'Follow-up Criteria'
    _columns = {
        'name': fields.char('Follow-Up Action', size=64, required=True),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of follow-up lines."),
        'delay': fields.integer('Due Days', help="The number of days after the due date of the invoice to wait before sending the reminder.  Could be negative if you want to send a polite alert beforehand.", required=True),
        'followup_id': fields.many2one('insurance_followup.followup', 'Follow Ups', required=True, ondelete="cascade"),
        'description': fields.text('Printed Message', translate=True),
        'send_email':fields.boolean('Send an Email', help="When processing, it will send an email"),
        'email_template_id':fields.many2one('email.template', 'Email Template', ondelete='set null'),
        'state': fields.selection([
            ('before','Before'),
            ('after','After'),
            ],'Status', select=True,required=True),
    }
    _order = 'sequence'
    _sql_constraints = [('days_uniq', 'unique(followup_id, delay)', 'Days of the follow-up levels must be different')]
    _defaults = {
        'send_email': True,
    }

insurance_followup_followup_line()


class insurance_issuer(osv.osv):
    _name = 'insurance.issuer'
    _columns = {
		'name': fields.char('Name'),
	}
insurance_issuer()



