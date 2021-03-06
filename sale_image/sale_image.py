# -*- coding: utf-8 -*-
##############################################################################
#
#    Product Images on sale order line and Delivery Order line.
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

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class stock_move(osv.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'

    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        res_prod = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id, loc_id,loc_dest_id, partner_id)
        prod_obj = self.pool.get('product.product')
        obj = prod_obj.browse(cr, uid, prod_id)
        res_prod['value'].update({'prod_image': obj.image_small})
        return res_prod
    

    _columns = {
		'prod_image' : fields.binary('Product Image'),
	}

stock_move()

class sale_order_line(osv.Model):
	_name = 'sale.order.line'
	_inherit = 'sale.order.line'
	_columns = {
		'prod_image' : fields.binary('Product Image'),
		}
		
	def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
	uom=False, qty_uos=0, uos=False, name='', partner_id=False,
	lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False,prod_image=False, context=None):
		context = context or {}
		product_uom_obj = self.pool.get('product.uom')
		partner_obj = self.pool.get('res.partner')
		product_obj = self.pool.get('product.product')
		warning = {}
		res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
		uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
		lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
		if not product:
			res['value'].update({'product_packaging': False})
			return res

		#update of result obtained in super function
		res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
		res['value'].update(res_packing.get('value', {}))
		warning_msgs = res_packing.get('warning') and res_packing['warning']['message'] or ''
		product_obj = product_obj.browse(cr, uid, product, context=context)
		res['value']['delay'] = (product_obj.sale_delay or 0.0)
		res['value']['type'] = product_obj.procure_method

		#check if product is available, and if not: raise an error
		uom2 = False
		if uom:
			uom2 = product_uom_obj.browse(cr, uid, uom)
		if product_obj.uom_id.category_id.id != uom2.category_id.id:
			uom = False
		if not uom2:
			uom2 = product_obj.uom_id
		compare_qty = float_compare(product_obj.virtual_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
		if (product_obj.type=='product') and int(compare_qty) == -1 \
		and (product_obj.procure_method=='make_to_stock'):
			warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
			(qty, uom2 and uom2.name or product_obj.uom_id.name,
			max(0,product_obj.virtual_available), product_obj.uom_id.name,
			max(0,product_obj.qty_available), product_obj.uom_id.name)
			warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"

		#update of warning messages
		if warning_msgs:
			warning = {
			'title': _('Configuration Error!'),
			'message' : warning_msgs
			}
		res.update({'warning': warning})
		res['value']['prod_image'] =  product_obj.image_small or False
		return res


sale_order_line()

class sale_order(osv.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'

	def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
		location_id = order.shop_id.warehouse_id.lot_stock_id.id
		output_id = order.shop_id.warehouse_id.lot_output_id.id
		return {
			'name': line.name,
			'picking_id': picking_id,
			'product_id': line.product_id.id,
			'prod_image':line.prod_image,
			'date': date_planned,
			'date_expected': date_planned,
			'product_qty': line.product_uom_qty,
			'product_uom': line.product_uom.id,
			'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
			'product_uos': (line.product_uos and line.product_uos.id)\
				or line.product_uom.id,
			'product_packaging': line.product_packaging.id,
			'partner_id': line.address_allotment_id.id or order.partner_shipping_id.id,
			'location_id': location_id,
			'location_dest_id': output_id,
			'sale_line_id': line.id,
			'tracking_id': False,
			'state': 'draft',
			#'state': 'waiting',
			'company_id': order.company_id.id,
			'price_unit': line.product_id.standard_price or 0.0
		}
sale_order()
	
class purchase_order_line(osv.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'
    _columns = {
        'prod_image' : fields.binary('Product Image'),
    }
    def onchange_product_uom(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
        """
        onchange handler of product_uom.
        """
        if not uom_id:
            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        
        return self.onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit,prod_image=False, context=context)

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,partner_id, date_order=False,fiscal_position_id=False, date_planned=False,name=False, price_unit=False,prod_image=False, context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_supplierinfo = self.pool.get('product.supplierinfo')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
        if product.description_purchase:
            name += '\n' + product.description_purchase
        res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.date.context_today(self,cr,uid,context=context)

        supplierinfo = False
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if (qty or 0.0) < min_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        # - determine price_unit and taxes_id
        if pricelist_id:
            price = product_pricelist.price_get(cr, uid, [pricelist_id],
                    product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order})[pricelist_id]
        else:
            price = product.standard_price

        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})
        res['value']['prod_image'] =  product.image_small or False
        return res

    product_id_change = onchange_product_id
    product_uom_change = onchange_product_uom

purchase_order_line()

class purchase_order(osv.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
        return {
            'name': order_line.name or '',
            'product_id': order_line.product_id.id,
            'prod_image':order_line.prod_image,
            'product_qty': order_line.product_qty,
            'product_uos_qty': order_line.product_qty,
            'product_uom': order_line.product_uom.id,
            'product_uos': order_line.product_uom.id,
            'date': self.date_to_datetime(cr, uid, order.date_order, context),
            'date_expected': self.date_to_datetime(cr, uid, order_line.date_planned, context),
            'location_id': order.partner_id.property_stock_supplier.id,
            'location_dest_id': order.location_id.id,
            'picking_id': picking_id,
            'partner_id': order.dest_address_id.id or order.partner_id.id,
            'move_dest_id': order_line.move_dest_id.id,
            'state': 'draft',
            'type':'in',
            'purchase_line_id': order_line.id,
            'company_id': order.company_id.id,
            'price_unit': order_line.price_unit
        }
purchase_order()
