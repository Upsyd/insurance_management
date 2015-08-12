from openerp.report import report_sxw
from openerp.osv import osv
from datetime import time,date,datetime,timedelta

class insurance_followup_report(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        super(insurance_followup_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time' : time,
                                  'ids_to_objects' : self.ids_to_objects,
                                  })
                                  
    def ids_to_objects(self, form):
        list_obj = []
        for obj in self.pool.get('insurance.followup').browse(self.cr, self.uid, form):
            list_obj.append(obj)
        print '\n in ids_to_objects',form,list_obj
        return list_obj
        
class insurance_followup_report_template_id(osv.AbstractModel):
    _name='report.insurance_management.insurance_followup_report_template_id'
    _inherit='report.abstract_report'
    _template='insurance_management.insurance_followup_report_template_id'
    _wrapped_report_class=insurance_followup_report
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
