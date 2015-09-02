# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.report import report_sxw
from openerp.osv import osv
from datetime import time, date, datetime, timedelta


class insurance_followup_report_all(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(insurance_followup_report_all, self).__init__(
            cr, uid, name, context=context)
        self.index = 0
        self.localcontext.update({
            'time': time,
            'ids_to_objects': self.ids_to_objects,
            'ids_to_payment': self._ids_to_payment,
        })

    def ids_to_objects(self, form):
        list_obj = []
        for obj in self.pool.get('insurance.followup').browse(self.cr, self.uid, form):
            list_obj.append(obj)
        return list_obj

    def _ids_to_payment(self, ins_obj):
        textfreq = None
        frequency = ins_obj.payment_frequency or 0
        ids = self.pool.get('payment.frequency').search(self.cr, self.uid, [])
        for line in self.pool.get('payment.frequency').browse(self.cr, self.uid, ids):
            freq_no = line.no
            freq_desc = line.desc
            if frequency == int(freq_no):
                textfreq = freq_desc
        return textfreq


class insurance_followup_report_all_template_id(osv.AbstractModel):
    _name = 'report.insurance_management.insurance_followup_report_all_template_id'
    _inherit = 'report.abstract_report'
    _template = 'insurance_management.insurance_followup_report_all_template_id'
    _wrapped_report_class = insurance_followup_report_all


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
