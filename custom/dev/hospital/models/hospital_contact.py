from odoo import fields, models


class EmergencyContact(models.Model):
    _inherit = 'hospital.person'
    _name = 'hospital.contact'
    _description = 'Emergency Contact'
