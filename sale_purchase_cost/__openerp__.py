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

{
    'name': 'Sale Purchase Cost',
    'version': '1.0',
    'category': 'Sale Purchase Cost',
    'sequence': 14,
    'summary': 'Sale Purchase Cost',
    'description': """
Manage sales quotations and orders with Sales Currency
==================================
Sales Cost
    """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    'images': [],
    'depends': ['account_voucher','sale','purchase'],
    'data': [
        'sale_purchase_cost_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

