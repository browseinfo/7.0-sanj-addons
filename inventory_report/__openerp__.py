# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

{
    'name':' Stock Inventory Report',
    'version':'7.0',
    'author':'BrowseInfo',
    'website':'http://www.browseinfo.in',
    'images':[],
    'data': [
              'products_report_view.xml','report/stock_picking_in_report_view.xml',
            ],
    'depends':['stock','report_aeroo','sale'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

