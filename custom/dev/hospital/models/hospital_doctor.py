from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(string='Specialty', required=True)
