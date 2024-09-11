from odoo import fields, models


class Person(models.AbstractModel):
    _name = 'hospital.person'
    _description = 'Abstract Person Model'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', required=True)
