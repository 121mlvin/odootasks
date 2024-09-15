from odoo import fields, models
from odoo.exceptions import ValidationError


class RescheduleAppointmentWizard(models.TransientModel):
    _name = 'hospital.reschedule.appointment.wizard'
    _description = 'Reschedule Appointment Wizard'

    visit_id = fields.Many2one('hospital.visit', string='Original Appointment', required=True)
    new_appointment_date = fields.Datetime(string='New Appointment Date', required=True)
    new_doctor_id = fields.Many2one('hospital.doctor', string='New Doctor')

    def action_reschedule_appointment(self):
        if not self.new_doctor_id:
            self.new_doctor_id = self.visit_id.doctor_id

        existing_visits = self.env['hospital.visit'].search([
            ('doctor_id', '=', self.new_doctor_id.id),
            ('appointment_date', '=', self.new_appointment_date),
            ('id', '!=', self.visit_id.id)
        ])

        if existing_visits:
            raise ValidationError('The selected doctor is already booked for this time slot.')

        self.visit_id.appointment_date = self.new_appointment_date
        self.visit_id.doctor_id = self.new_doctor_id
