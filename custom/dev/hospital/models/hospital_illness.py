from odoo import models, fields


class Illness(models.Model):
    _name = 'hospital.illness'
    _description = 'Illness Catalog'

    name = fields.Char(string='Illness Name', required=True)
    type_id = fields.Many2one('hospital.illness.type', string='Illness Type')
