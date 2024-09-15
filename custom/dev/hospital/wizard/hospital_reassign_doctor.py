from odoo import fields, models


class ReassignPersonalDoctorWizard(models.TransientModel):
    _name = 'hospital.reassign.doctor.wizard'
    _description = 'Reassign Personal Doctor Wizard'

    new_doctor_id = fields.Many2one('hospital.doctor', string='New Doctor', required=True)
    patient_ids = fields.Many2many('hospital.patient', string='Patients')

    def action_reassign_doctor(self):
        for patient in self.patient_ids:
            patient.personal_doctor_id = self.new_doctor_id
