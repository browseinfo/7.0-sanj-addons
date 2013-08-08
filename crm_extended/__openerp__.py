# -*- coding: utf-8 -*-
##############################################################################
#
#    Customer Relationship management extended
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
    'name': 'Crm Extended',
    'version': '1.0',
    'category': 'Crm',
    'sequence': 14,
    'summary': 'Crm Extended',
    'description': """
Manage crm and send mail
==================================
* send mail
    """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    'images': [],
    'depends': ['crm', 'product'],
    'data': [
        'crm_extended_view.xml',
        'crm_extended_template_data.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

