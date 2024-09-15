from odoo import fields, models


class DoctorDailyScheduleWizard(models.TransientModel):
    _name = 'hospital.doctor.daily.schedule.wizard'
    _description = 'Doctor Daily Schedule Wizard'

    wizard_id = fields.Many2one('hospital.doctor.weekly.schedule.wizard', string='Wizard Reference')
    date = fields.Datetime(string='Date', required=True)
