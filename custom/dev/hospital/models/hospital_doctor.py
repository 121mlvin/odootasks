from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'hospital.person'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(string='Specialty', required=True)
    is_intern = fields.Boolean(string='Is Intern', default=False)
    mentor_id = fields.Many2one('hospital.doctor', string='Mentor Doctor', domain="[('is_intern', '=', False)]")

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for doctor in self:
            if doctor.is_intern and doctor.mentor_id.is_intern:
                raise ValidationError('Mentor cannot be an intern.')
