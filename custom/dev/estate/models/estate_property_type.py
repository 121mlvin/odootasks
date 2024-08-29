from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'Type name must be unique'),
    ]
