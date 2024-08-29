from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'Tag name must be unique'),
    ]
