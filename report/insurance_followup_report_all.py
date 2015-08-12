from openerp.report import report_sxw
from openerp.osv import osv
from datetime import time,date,datetime,timedelta

class insurance_followup_report_all(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        super(insurance_followup_report_all, self).__init__(cr, uid, name, context=context)
        self.index = 0
        self.localcontext.update({
                                  'time' : time,
                                  'ids_to_objects' : self.ids_to_objects,
                                  'ids_to_payment' : self._ids_to_payment,
                                  })
                                  
    def ids_to_objects(self, form):
        list_obj = []
        for obj in self.pool.get('insurance.followup').browse(self.cr, self.uid, form):
            list_obj.append(obj)
        print '\n in ids_to_objects',form,list_obj
        return list_obj
        
    def _ids_to_payment(self, ins_obj):
        print '\n form of report all',ins_obj
        textfreq = None
        frequency = ins_obj.payment_frequency or 0
        ids = self.pool.get('payment.frequency').search(self.cr,self.uid,[])
        for line in self.pool.get('payment.frequency').browse(self.cr, self.uid, ids):
            freq_no = line.no
            freq_desc = line.desc
            if frequency == int(freq_no):
                textfreq = freq_desc
        print '\n _ids_to_payment of report all',textfreq
        return textfreq
        
class insurance_followup_report_all_template_id(osv.AbstractModel):
    _name='report.insurance_management.insurance_followup_report_all_template_id'
    _inherit='report.abstract_report'
    _template='insurance_management.insurance_followup_report_all_template_id'
    _wrapped_report_class=insurance_followup_report_all
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
