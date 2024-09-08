from odoo import models, fields, api


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Patient Diagnosis'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    # illness_id =
    treatment = fields.Text(string='Treatment Prescribed')
    diagnosis_date = fields.Date(string='Diagnosis Date', required=True, default=fields.Date.today())
