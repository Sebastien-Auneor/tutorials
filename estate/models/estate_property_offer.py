from datetime import timedelta
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Offer Price', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', default='pending', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)    
    
    validity = fields.Integer(string='Validity (days)', compute='_compute_validity', inverse='_inverse_date_deadline')
    date_deadline = fields.Date(string='Deadline')
    
    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'The offer price must be positive.')
    ]

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (record.date_deadline - record.create_date.date()).days
                else:  # in case create_date is not set yet
                    record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    @api.onchange('validity')
    def _inverse_date_deadline(self):
        for record in self:
            if record.validity:
                if record.create_date:
                    record.date_deadline = record.create_date + timedelta(days=record.validity)
                else: # in case create_date is not set yet
                    record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()
    
    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            
            # Refuse other offers on the same property
            other_offers = self.search([('property_id', '=', record.property_id.id), ('id', '!=', record.id)])
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
    