from odoo import models, fields, api
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Information'
    _inherit = 'hospital.person'

    date_of_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    passport_info = fields.Char(string='Passport Details')
    contact_person_id = fields.Many2one('hospital.contact', string='Emergency Contact', required=True)
    personal_doctor_id = fields.Many2one('hospital.doctor', string='Personal Doctor')

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.date_of_birth:
                birth_date = patient.date_of_birth
                age_in_years = today.year - birth_date.year
                has_birthday_passed = (today.month, today.day) >= (birth_date.month, birth_date.day)
                patient.age = age_in_years if has_birthday_passed else age_in_years - 1
            else:
                patient.age = 0

    @api.model
    def create(self, vals):
        patient = super(HospitalPatient, self).create(vals)
        if vals.get('personal_doctor_id'):
            self.env['hospital.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': vals.get('personal_doctor_id'),
            })
        return patient

    def write(self, vals):
        result = super(HospitalPatient, self).write(vals)
        if vals.get('personal_doctor_id'):
            for patient in self:
                self.env['hospital.doctor.history'].create({
                    'patient_id': patient.id,
                    'doctor_id': vals.get('personal_doctor_id'),
                })
        return result
