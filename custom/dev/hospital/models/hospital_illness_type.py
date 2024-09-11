from odoo import models, fields


class IllnessType(models.Model):
    _name = 'hospital.illness.type'
    _description = 'Illness Type'

    name = fields.Char(string='Illness Type', required=True)
    parent_id = fields.Many2one('hospital.illness.type', string='Parent Illness Type')
    child_ids = fields.One2many('hospital.illness.type', 'parent_id', string='Subtypes')