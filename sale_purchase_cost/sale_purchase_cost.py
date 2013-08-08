# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Purchase Fabrication and installtion cost
#    Copyright (C) 2004-2010 Browse Info Pvt Ltd (<http://www.browseinfo.in>).
#    $autor:
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
from openerp.osv import osv, fields
from twisted.application.strports import _DEFAULT
import openerp.addons.decimal_precision as dp

class sale_order_line(osv.osv):

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price = price + line.fabrication_cost + line.installation_cost
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    _inherit = 'sale.order.line'
    _columns = {

        'fabrication': fields.selection([('without_fabrication_labour', 'Without Fabrication Labour'), ('with_fabrication_labour', 'With Fabrication Labour')], 'Fabrication'),
        'fabrication_cost': fields.float('Fabrication Cost'),
        'installation': fields.selection([('without_installation', 'Without Installation'), ('with_installation', 'With Installation')], 'Installation'),
        'installation_cost': fields.float('Installation Cost'),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')), 
    }
    _defaults = {
        'fabrication': lambda *args: 'without_fabrication_labour',
        'installation': lambda *args: 'without_installation',
    }
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = {}
        if not line.invoiced:
            if not account_id:
                if line.product_id:
                    account_id = line.product_id.property_account_income.id
                    if not account_id:
                        account_id = line.product_id.categ_id.property_account_income_categ.id
                    if not account_id:
                        raise osv.except_osv(_('Error!'),
                                _('Please define income account for this product: "%s" (id:%d).') % \
                                    (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_account_income_categ', 'product.category',
                            context=context)
                    account_id = prop and prop.id or False
            uosqty = self._get_line_qty(cr, uid, line, context=context)
            uos_id = self._get_line_uom(cr, uid, line, context=context)
            pu = 0.0
            if uosqty:
                pu = round(line.price_unit * line.product_uom_qty / uosqty,
                        self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
                if line.fabrication_cost:
                    pu = pu +  line.fabrication_cost
                if line.installation_cost:
                    pu = pu + line.installation_cost
            fpos = line.order_id.fiscal_position or False
            account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
            if not account_id:
                raise osv.except_osv(_('Error!'),
                            _('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
            res = {
                'name': line.name,
                'sequence': line.sequence,
                'origin': line.order_id.name,
                'account_id': account_id,
                'price_unit': pu,
                'quantity': uosqty,
                'discount': line.discount,
                'uos_id': uos_id,
                'product_id': line.product_id.id or False,
                'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
                'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
            }

        return res

    
class purchase_order_line(osv.osv):
    _inherit='purchase.order.line'
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)
            tot = taxes.get('total')
            tot = tot + line.fabrication_cost + line.installation_cost
            taxes['total'] = tot
            #taxes = taxes + line.fabrication_cost + line.installation_cost
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    _columns = {
        'fabrication': fields.selection([('without_fabrication_labour', 'Without Fabrication Labour'), ('with_fabrication_labour', 'With Fabrication Labour')], 'Fabrication'),
        'fabrication_cost': fields.float('Fabrication Cost'),
        'installation': fields.selection([('without_installation', 'Without Installation'), ('with_installation', 'With Installation')], 'Installation'),
        'installation_cost': fields.float('Installation Cost'),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
    }
    _defaults = {
        'fabrication': lambda *args: 'without_fabrication_labour',
        'installation': lambda *args: 'without_installation',
    }
class purchase_order(osv.osv):
    _inherit='purchase.order'
    
    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        """Collects require data from purchase order line that is used to create invoice line
        for that purchase order line
        :param account_id: Expense account of the product of PO line if any.
        :param browse_record order_line: Purchase order line browse record
        :return: Value for fields of invoice lines.
        :rtype: dict
        """
        total_price = order_line.price_unit
        if order_line.fabrication_cost:
            total_price = total_price +  order_line.fabrication_cost
        if order_line.installation_cost:
            total_price = total_price + order_line.installation_cost
        return {
            'name': order_line.name,
            'account_id': account_id,
            'price_unit': total_price or 0.0,
            'quantity': order_line.product_qty,
            'product_id': order_line.product_id.id or False,
            'uos_id': order_line.product_uom.id or False,
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            'account_analytic_id': order_line.account_analytic_id.id or False,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
