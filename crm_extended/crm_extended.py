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

from openerp.osv import osv, fields
#from twisted.application.strports import _DEFAULT

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'interested': fields.char('Interested', size=64),
        'activities': fields.char('Activities', size=64),
        'birth_date': fields.date('Birth-Date'),
    }

res_partner()

class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
        'interested': fields.char('Interested', size=64),
        'activities': fields.char('Activities', size=64),
        'birth_date': fields.date('Birth-Date'), 
        'product_ids': fields.many2many('product.product', 'crm_product_product_rel', 'crm_id','product_id', 'Interested Products'),
    }

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        result = {}
        values = {}
        if partner_id: 
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            values = {
                'partner_name' : partner.name,
                'street' : partner.street,
                'street2' : partner.street2,
                'city' : partner.city,
                'state_id' : partner.state_id and partner.state_id.id or False,
                'country_id' : partner.country_id and partner.country_id.id or False,
                'email_from' : partner.email,
                'phone' : partner.phone,
                'mobile' : partner.mobile,
                'fax' : partner.fax,
                'interested' : partner.interested,
                'activities': partner.activities,
                'birth_date': partner.birth_date,
            }
        return {'value' : values}

    def action_crm_lead_send_mail(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the project task template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm_extended', 'email_template_crm_lead')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict(context)
        ctx.update({
            'default_model': 'crm.lead',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

crm_lead()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
