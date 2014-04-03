# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################
from datetime import datetime
import time
from collections import defaultdict
from openerp.report import report_sxw

class inventory_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(inventory_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
        })


report_sxw.report_sxw('report.inventory.report', 'stock.inventory', 'inventory_report/report/inventory_report.rml.rml',           parser=inventory_report, header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
