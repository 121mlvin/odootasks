from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer Model'
    _order = 'price desc'

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
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive'),
    ]

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

    def action_accept(self):
        if self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
            raise UserError("An offer has already been accepted for this property.")

        if self.property_id.state in ['sold', 'canceled']:
            raise UserError("You cannot accept an offer for a property that is already sold or canceled.")

        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        offer_price = vals.get('price')

        if property_id and offer_price:
            property_record = self.env['estate.property'].browse(property_id)

            for existing_offer in property_record.offer_ids:
                if existing_offer.price >= offer_price:
                    raise UserError("An offer already exists with a higher or equal amount.")

            new_offer = super().create(vals)
            property_record.state = 'offer_received'
            return new_offer

        else:
            raise UserError("Property and offer price must be specified.")
