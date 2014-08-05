import time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from openerp.osv import osv, fields
from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _
from openerp import netsvc
import openerp.addons.decimal_precision as dp

class project_project(osv.osv):
#     def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
#         tax_obj = self.pool.get('account.tax')
#         cur_obj = self.pool.get('res.currency')
#         sale_line = self.pool.get('sale.order.line')
#         res = {}
#         if context is None:
#             context = {}
#         for line in sale_line.browse(cr, uid, ids, context=context):
#             price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#             price = price + line.fabrication_cost + line.installation_cost
#             taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
#             cur = line.order_id.pricelist_id.currency_id
#             res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
#         return res
    
    _inherit = 'project.project'
    
    _columns = {
        'schedule_delivery_date': fields.date('Installation Date'),
        'fabrication': fields.selection([('without_fabrication_labour', 'Without Fabrication Labour'), ('with_fabrication_labour', 'With Fabrication Labour')], 'Fabrication'),
        'fabrication_cost': fields.float('Fabrication Cost'),
        'installation': fields.selection([('without_installation', 'Without Installation'), ('with_installation', 'With Installation')], 'Installation'),
        'installation_cost': fields.float('Installation Cost'),
#        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')), 
    }
    
    _defaults = {
        'fabrication': lambda *args: 'without_fabrication_labour',
        'installation': lambda *args: 'without_installation',
    }

    def run_scheduled_date_cron(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        if context is None:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        mail_to = ""
        mail_ids = []
        
        admin_email = self.pool.get('res.users').browse(cr, uid, [1])[0].email
        
        project_ids = self.search(cr, uid, [('state', '=', 'open')], context=context)
        for project in self.browse(cr, uid, project_ids, context=context):
            schedule_date = project.schedule_delivery_date
            manager = project.user_id.email or False
            next_7th_date = datetime.strptime(schedule_date, '%Y-%m-%d') + relativedelta(days=7)
            next_date = next_7th_date.strftime('%Y-%m-%d')
            today = time.strftime('%Y-%m-%d')
            to = ''
            for mail in project.members:
                toteam = mail.email 
                to += manager +  toteam + ','
                if today < schedule_date and schedule_date < next_date:
                    sub = '[Next Scheduled Date For project]'
                    body = """
    Hello ,
    Just a friendly reminder you ,A Project %s 's Next Scheduled Date on: %s.""" % (project.name,next_date)
                    mail_to = to
                    if mail_to:
                        vals = {
                                'state': 'outgoing',
                                'subject': sub,
                                'body_html': body,
                                'email_to': mail_to,
                                'email_from': admin_email,
                            }
                       
                        mail_ids.append(mail_mail.create(cr, uid, vals, context=context))
                        mail_mail.send(cr, uid, mail_ids, auto_commit=True, context=context)
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
