from odoo import models, fields


class PersonalDoctorHistory(models.Model):
    _name = 'hospital.doctor.history'
    _description = 'Personal Doctor History'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    assignment_date = fields.Datetime(string='Assignment Date', default=fields.Datetime.now)
