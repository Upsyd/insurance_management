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
from openerp import netsvc
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from datetime import datetime

class insurance_followup_send_mail(osv.osv_memory):
    _name = 'insurance_followup.send.mail'
    _description = 'Send Mail to Customers'
    _columns = {
        'date': fields.datetime('Follow-up Sending Date', required=True, 
                            help="This field allow you to select a forecast date to plan your follow-ups"),
        'followup_id': fields.many2one('insurance_followup.followup', 'Follow-Up', required=True, readonly = True),
        'company_id':fields.related('followup_id', 'company_id', type='many2one',
                                    relation='res.company', store=True, readonly=True),
        'print_option': fields.selection([('print_any', 'Selected Insurnace Report'), ('print_all', 'All Insurnace Report')], 'Report Preference', required=True),
        'insurance_ids': fields.many2many('insurance.followup', 'insurance_mail_rel', 'followup_id', 'insurance_id', 'Insurance'),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
    }


    def _get_followup(self, cr, uid, context=None):
        if context is None:
            context = {}
        if context.get('active_model', 'ir.ui.menu') == 'insurance_followup.followup':
            return context.get('active_id', False)
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        followp_id = self.pool.get('insurance_followup.followup').search(cr, uid, [('company_id', '=', company_id)], context=context)
        print "£££££££££££££££££££££££",followp_id
        return followp_id and followp_id[0] or False
        

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'followup_id': _get_followup,
        'print_option': 'print_all',
        'date_start': lambda *a: time.strftime('%Y-%m-%d'),
        'date_end': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def do_process(self, cr, uid, ids, context=None):
        followup_obj = self.pool.get('insurance.followup')
        ins_obj = self.pool.get('insurance_followup.send.mail')
        Model_obj = self.pool.get('ir.model.data')
        Email_tem_obj = self.pool.get('email.template')
        date_format = "%Y-%m-%d %H:%M:%S"
        followup_id = ins_obj.browse(cr, uid, ids, context=context)[0].followup_id
        date = ins_obj.browse(cr, uid, ids, context=context)[0].date
        wiz_date = datetime.strptime(date, date_format)
        #fifty_to_five = [25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
        ten_to_fifty = [11,12,13,14,15]
        six_to_ten = [6,7,8,9,10]
        one_to_five = [1,2,3,4,5]
        one_to_two = [1,2]
        ten_to_twentytwo = [20,21,22]

        followup_ids =  followup_obj.search(cr, uid, [('state', 'in', ['draft', 'open'])], context=context)
        for followup in followup_obj.browse(cr, uid, followup_ids, context=context):
            wf_service = netsvc.LocalService("workflow")
            print '\n followup.date_due',followup.date_due
            due_date= datetime.strptime(followup.date_due, "%Y-%m-%d")
            delta = wiz_date - due_date
            gema =  due_date - wiz_date
            print '\n delta and gema',delta,gema
            days_before = gema.days
            day_after = delta.days
            for line in followup_id.followup_line:
                if line.state == 'before':
                    #if days_before in fifty_to_five:
                        #mail_message = self.pool.get('email.template').send_mail(cr,uid,line.email_template_id,followup.id,force_send=True)
                    if days_before in ten_to_fifty:
                        print '\n ten_to_fifty',days_before
                        template_id = Model_obj.get_object_reference(cr, uid, 'insurance_management', 'email_template_insurance_followup_level_before15')[1]
                        
                        mail_message = Email_tem_obj.send_mail(cr, uid, template_id, followup.id, force_send=True, context=context)
                        
                        break
                    elif days_before in six_to_ten:
                        print '\n six_to_ten',days_before
                        template_id = Model_obj.get_object_reference(cr, uid, 'insurance_management', 'email_template_insurance_followup_level_before10')[1]
                        
                        mail_message = Email_tem_obj.send_mail(cr, uid, template_id, followup.id, force_send=True, context=context)
                        break
                    elif days_before in one_to_five:
                        print '\n one_to_five',days_before
                        template_id = Model_obj.get_object_reference(cr, uid, 'insurance_management', 'email_template_insurance_followup_level_before5')[1]
                        
                        mail_message = Email_tem_obj.send_mail(cr,uid,template_id,followup.id,force_send=True)
                        break
                if line.state == 'after':
                    if day_after in one_to_two:
                        print '\n one_to_two',day_after
                        template_id = Model_obj.get_object_reference(cr, uid, 'insurance_management', 'email_template_insurance_followup_level_after1')[1]
                        
                        mail_message = Email_tem_obj.send_mail(cr,uid,template_id,followup.id,force_send=True)
                        break
                    elif day_after in ten_to_twentytwo:
                        print '\n ten_to_twentytwo',day_after
                        template_id = Model_obj.get_object_reference(cr, uid, 'insurance_management', 'email_template_insurance_followup_level_after22')[1]
                        
                        mail_message = Email_tem_obj.send_mail(cr,uid,template_id,followup.id,force_send=True)
                        wf_service.trg_validate(uid, 'insurance.followup', followup.id, 'insurance_cancel', cr)
                        break
        return True

    def print_report(self, cr, uid, ids, context=None):
        print '\n in report print'
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = {}
        followup_obj = self.pool.get('insurance.followup')
        date_format = "%Y-%m-%d"
        followup_id = self.browse(cr, uid, ids, context=context)[0].followup_id
        date = self.browse(cr, uid, ids, context=context)[0].date
        wiz_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        fifty_to_five = [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
        followup_print_ids = []
        line_ids = []
        followup_ids =  followup_obj.search(cr, uid, [('state', 'in', ['draft', 'open'])], context=context)
        print '\n print report',followup_ids
        for followup in followup_obj.browse(cr, uid, followup_ids, context=context):
            wf_service = netsvc.LocalService("workflow")
            if followup.date_due:
                due_date= datetime.strptime(followup.date_due, date_format)
                gema =  due_date - wiz_date
                delta = wiz_date - due_date
                days_before = gema.days
                for line in followup_id.followup_line:
                    if line.state == 'before':
                        if days_before in fifty_to_five or line.delay in fifty_to_five:
                            followup_print_ids.append(followup.id)
                            line_ids.append(line.id)
                            break
        data['partner_ids'] = followup_print_ids
        data['line_ids'] = line_ids
        print '\n in report print',data
        #if not (line_ids and followup_print_ids):
        #   raise osv.except_osv(_('No data!'), _('No Matching Record Found'))
        datas = {
             'ids': [],
             'model': 'insurance.followup',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'insurance_management.insurance_followup_report_template_id',
            'datas': datas,
        }

    def print_report_preference(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}

        data = {}
        followup_obj = self.pool.get('insurance.followup')
        date_format = "%Y-%m-%d"
        followup_id = self.browse(cr, uid, ids, context=context)[0].followup_id
        date = self.browse(cr, uid, ids, context=context)[0].date
        wiz_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        fifty_to_five = [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
        followup_print_ids = []
    
        current_id = self.browse(cr, uid, ids[0], context=context)

        line_ids = []
        followup_ids =  followup_obj.search(cr, uid, [('state', 'in', ['draft', 'open'])], context=context)
        for followup in current_id.insurance_ids:
            wf_service = netsvc.LocalService("workflow")
            if followup.date_due:
                due_date= datetime.strptime(followup.date_due, date_format)
                gema =  due_date - wiz_date
                delta = wiz_date - due_date
                days_before = gema.days
                for line in followup_id.followup_line:
                    if line.state == 'before':
                        if days_before in fifty_to_five or line.delay in fifty_to_five:
                            followup_print_ids.append(followup.id)
                            line_ids.append(line.id)
        data['partner_ids'] = followup_print_ids
        data['line_ids'] = line_ids
        print '\n data of report preference',data
        datas = {
             'ids': [],
             'model': 'insurance.followup',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'insurance_management.insurance_followup_report_all_template_id',
            'datas': datas,
       }


    def print_all_report(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = {}
        followup_obj = self.pool.get('insurance.followup')
        date_format = "%Y-%m-%d"
        followup_id = self.browse(cr, uid, ids, context=context)[0].followup_id
        date = self.browse(cr, uid, ids, context=context)[0].date
        wiz_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        fifty_to_five = [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
        followup_print_ids = []
        line_ids = []
        followup_ids =  followup_obj.search(cr, uid, [('state', 'in', ['draft', 'open'])], context=context)

        for followup in followup_obj.browse(cr, uid, followup_ids, context=context):
            wf_service = netsvc.LocalService("workflow")
            if followup.date_due:
                due_date= datetime.strptime(followup.date_due, date_format)
                gema =  due_date - wiz_date
                delta = wiz_date - due_date
                days_before = gema.days
                for line in followup_id.followup_line:
                    if line.state == 'before':
                        if days_before in fifty_to_five or line.delay in fifty_to_five:
                            followup_print_ids.append(followup.id)
                            line_ids.append(line.id)
                            break
        data['partner_ids'] = followup_print_ids
        data['line_ids'] = line_ids
        print '\n print all reports',data
        datas = {
             'ids': [],
             'model': 'insurance.followup',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name':  'insurance_management.insurance_followup_report_all_template_id',
            'datas': datas,
       }

    def print_all_report_date_range(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = {}

        followup_obj = self.pool.get('insurance.followup')
        date_format = "%Y-%m-%d"

        inv_ids = followup_obj.search(cr, uid, [])

        startdate = self.browse(cr, uid, ids, context=context)[0].date_start
        enddate = self.browse(cr, uid, ids, context=context)[0].date_end
        followup_print_ids = []
        line_ids = []

        for inv_id in inv_ids:
            if inv_id:
                followup = followup_obj.browse(cr, uid, inv_id, context=context)
                if followup.date_due:
                    wizard_start_date = datetime.strptime(startdate, '%Y-%m-%d')
                    wizard_end_date = datetime.strptime(enddate, '%Y-%m-%d')
                    followup_date = datetime.strptime(followup.date_due, '%Y-%m-%d')
    
                    if wizard_start_date.month <=  followup_date.month and wizard_end_date.month >=  followup_date.month and wizard_start_date.day <=  followup_date.day and wizard_end_date.day >=  followup_date.day:
                        followup_print_ids.append(followup.id)

        if not followup_print_ids:
            raise osv.except_osv(_('No data!'), _('No Matching Record Found'))

        data['partner_ids'] = followup_print_ids
        print '\n print all report from prefe',data
        datas = {
             'ids': [],
             'model': 'insurance.followup',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'insurance_management.insurance_followup_report_all_template_id',
            'datas': datas,
       }
           
insurance_followup_send_mail()



