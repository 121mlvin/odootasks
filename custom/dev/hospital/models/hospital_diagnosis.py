from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Patient Diagnosis'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    illness_id = fields.Many2one('hospital.illness', string='Illness', required=True)
    treatment = fields.Text(string='Treatment Prescribed')
    diagnosis_date = fields.Date(string='Diagnosis Date', required=True, default=fields.Date.today())
    mentor_comment = fields.Text(string='Mentor Comment')

    @api.constrains('doctor_id', 'mentor_comment')
    def _check_mentor_comment(self):
        for diagnosis in self:
            if diagnosis.doctor_id.is_intern and not diagnosis.mentor_comment:
                raise ValidationError('Mentor must write a comment for diagnoses made by an intern.')
