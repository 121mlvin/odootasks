from odoo import fields, models, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(
        string='Deadline Date',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 7