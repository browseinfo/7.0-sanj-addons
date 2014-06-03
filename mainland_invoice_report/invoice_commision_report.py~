# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv
from openerp.addons.decimal_precision import decimal_precision as dp
 
class account_invoice_commision_model(osv.osv):
    _name = "account.invoice.commision.model"
    _description = "Account Invoice Commision Report"
    _auto = False
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', domain=[('type','=','out_invoice')]),
        'user_id': fields.many2one('res.users', 'Salesperson', readonly=True),
        'total_commision': fields.float('Total Commision'),
        'commision': fields.float('Commision(%)'),
        'price_unit': fields.float('Unit Price'),
        'price_total': fields.float('Price Total'),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month',readonly=True),
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
    }
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'account_invoice_commision_model')
        cr.execute("""
            CREATE OR REPLACE VIEW account_invoice_commision_model AS(
            SELECT inv.id as id,
                    inv.partner_id,
                    inv.user_id,
                    line.commision,
                    line.price_unit,
                    inv.date_invoice as date,
                    to_char(inv.date_invoice, 'YYYY') as year,
                    to_char(inv.date_invoice, 'MM') as month,
                    sum(line.quantity * line.price_unit * (100.0-line.discount) / 100.0) as price_total,
                    (line.price_unit * line.commision / 100.0) as total_commision
            FROM 
                account_invoice inv
                join account_invoice_line line on (inv.id=line.invoice_id)
            where inv.type = 'out_invoice'
            group by
                inv.id,
                inv.partner_id,
                inv.user_id,
                inv.date_invoice,
                line.commision,
                line.price_unit,
                to_char(inv.date_invoice, 'YYYY'),
                to_char(inv.date_invoice, 'MM'),
                total_commision
                
            )
        """)
account_invoice_commision_model()
