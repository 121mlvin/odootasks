from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Date Availability',
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage?')
    garden = fields.Boolean(string='Garden?')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="The orientation of the garden"
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'

    )
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    salesman_id = fields.Many2one('res.users', string='Salesperson', index=True,
                                  default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area', compute="_compute_total", store=True)
    best_price = fields.Float(string='Best Offer', compute="_compute_best", store=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'A property selling price must be positive'),
    ]

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    def action_set_status_sold(self):
        if self.state != 'canceled':
            self.state = 'sold'
        else:
            raise UserError("A canceled property cannot be sold.")
        return True

    def action_set_status_canceled(self):
        self.state = 'canceled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def check_price_consistency(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                min_selling_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_selling_price, precision_rounding=0.01) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )

    @api.model
    def create(self, vals):
        print(vals)
        rtn = super().create(vals)
        print(rtn)
        return rtn

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("You can only delete properties in 'New' or 'Canceled' state.")
