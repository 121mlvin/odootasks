from odoo import models, fields


class DoctorSchedule(models.Model):
    _name = 'hospital.doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Date(string='Date', required=True)
    time = fields.Float(string='Time', required=True)

    _sql_constraints = [
        (
            'unique_doctor_schedule',
            'UNIQUE(doctor_id, date, time)',
            'A doctor cannot have two schedules starting at the same time on the same day.'
        )
    ]
