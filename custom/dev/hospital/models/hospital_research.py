from odoo import fields, models


class Research(models.Model):
    _name = 'hospital.research'
    _description = 'Research'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    research_type_id = fields.Many2one('hospital.research.type', string='Research Type', required=True)
    sample_id = fields.Many2one('hospital.sample.type', string='Sample Type', required=True)
    conclusions = fields.Text(string='Conclusions')
