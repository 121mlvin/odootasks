from odoo import fields, models


class DoctorWeeklyScheduleWizard(models.TransientModel):
    _name = 'hospital.doctor.weekly.schedule.wizard'
    _description = 'Doctor Weekly Schedule Wizard'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    week_type = fields.Selection([('even', 'Even Week'), ('odd', 'Odd Week'), ('both', 'Both')], string='Week Type',
                                 default='both', required=True)
    daily_schedule = fields.One2many('hospital.doctor.daily.schedule.wizard', 'wizard_id', string='Daily Schedule')

    def action_set_weekly_schedule(self):
        for day_schedule in self.daily_schedule:
            schedule_vals = {
                'doctor_id': self.doctor_id.id,
                'patient_id': self.patient_id.id,
                'appointment_date': day_schedule.date,
            }
            self.env['hospital.visit'].create(schedule_vals)
