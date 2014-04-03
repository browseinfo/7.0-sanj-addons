# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today Browseinfo (<http://www.browseinfo.in>).
#
##############################################################################

from osv import osv,fields
from openerp.osv import fields,osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class stock_inventory_line(osv.Model):
    _inherit = 'stock.inventory.line'
    _columns = {
        'physical_product_qty': fields.float('Physical Qty', digits_compute=dp.get_precision('Product Unit of Measure')),
    }

stock_inventory_line()

