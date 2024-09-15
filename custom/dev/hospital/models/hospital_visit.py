from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DoctorVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Doctor Visits'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    diagnosis_id = fields.Many2one('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    research_ids = fields.One2many('hospital.research', 'visit_id', string='Researches')
    appointment_completed = fields.Boolean(string='Appointment Completed', default=False)

    _sql_constraints = [
        (
            'unique_visit_schedule',
            'UNIQUE(doctor_id, appointment_date)',
            'This doctor is already booked for the selected date and time.'
        )
    ]

    @api.constrains('appointment_date', 'doctor_id')
    def _prevent_changes_if_completed(self):
        for visit in self:
            if visit.appointment_completed:
                raise ValidationError('You cannot change the date, time, or doctor for a completed appointment.')

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id:
                raise ValidationError('You cannot delete or archive doctor visits that are linked to a diagnosis.')
        return super(DoctorVisit, self).unlink()
