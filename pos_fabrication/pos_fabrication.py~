# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
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

from openerp.osv import osv, fields
#from twisted.application.strports import _DEFAULT
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class pos_order_line(osv.osv):
    _inherit = 'pos.order.line'
    
    def _amount_line_all(self, cr, uid, ids, prop, arg, context=None):
        res = dict([(i, {}) for i in ids])
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes_ids = [ tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id ]
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            
            if line.qty == 0.0:
                raise osv.except_osv(_('product quantity!'),
               _('You have to give product quantity at least 1 !' ))
            
            taxes = tax_obj.compute_all(cr, uid, taxes_ids, price, line.qty, product=line.product_id)
            
            total_included = taxes.get('total')
            total_included = total_included + ((line.fabrication_cost + line.installation_cost) * line.qty)
            taxes['total'] = total_included
            
            cur = line.order_id.pricelist_id.currency_id

            res[line.id]['price_subtotal'] = cur_obj.round(cr, uid, cur, taxes['total'])
            res[line.id]['price_subtotal_incl'] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
        
        
    _columns = {
        'fabrication': fields.selection([('without_fabrication_labour', 'Without Fabrication Labour'), ('with_fabrication_labour', 'With Fabrication Labour')], 'Fabrication'),
        'fabrication_cost': fields.float('Fabrication Cost'),
        'installation': fields.selection([('without_installation', 'Without Installation'), ('with_installation', 'With Installation')], 'Installation'),
        'installation_cost': fields.float('Installation Cost'),
        'price_subtotal': fields.function(_amount_line_all, multi='pos_order_line_amount', string='Subtotal w/o Tax', store=True),
        'price_subtotal_incl': fields.function(_amount_line_all, multi='pos_order_line_amount', string='Subtotal', store=True),
    }
    _defaults = {
        'fabrication': lambda *args: 'without_fabrication_labour',
        'installation': lambda *args: 'without_installation',
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
