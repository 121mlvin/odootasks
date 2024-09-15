from odoo import models, fields


class DiseaseReport(models.TransientModel):
    _name = 'disease.report'
    _description = 'Temporary Disease Report'

    disease_name = fields.Char(string='Disease')
    diagnosis_count = fields.Integer(string='Diagnosis Count')
