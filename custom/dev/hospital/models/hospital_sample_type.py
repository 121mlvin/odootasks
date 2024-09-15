from odoo import fields, models


class SampleType(models.Model):
    _name = 'hospital.sample.type'
    _description = 'Sample Type'

    name = fields.Char(string='Sample Type', required=True)
