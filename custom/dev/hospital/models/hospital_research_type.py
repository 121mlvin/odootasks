from odoo import fields, models


class ResearchType(models.Model):
    _name = 'hospital.research.type'
    _description = 'Research Type'

    name = fields.Char(string='Research Type', required=True)
    parent_id = fields.Many2one('hospital.research.type', string='Parent Research Type')
    child_ids = fields.One2many('hospital.research.type', 'parent_id', string='Subtypes')
