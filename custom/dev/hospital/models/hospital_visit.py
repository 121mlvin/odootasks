from odoo import fields, models


class DoctorVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Doctor Visits'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    diagnosis_id = fields.Many2one('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    research_ids = fields.One2many('hospital.research', 'visit_id', string='Researches')
