from odoo import models, fields, api
from datetime import datetime
import calendar


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    year = fields.Integer(string='Year', required=True, default=lambda self: datetime.now().year)
    month = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Month', required=True)

    def generate_report(self):
        self.ensure_one()

        first_day = f'{self.year}-{self.month}-01'
        last_day = f'{self.year}-{self.month}-{calendar.monthrange(self.year, int(self.month))[1]}'

        domain = [('diagnosis_date', '>=', first_day),
                  ('diagnosis_date', '<=', last_day)]
        diagnoses = self.env['hospital.diagnosis'].search(domain)

        report_data = {}
        for diagnosis in diagnoses:
            disease = diagnosis.illness_id.name
            if disease in report_data:
                report_data[disease] += 1
            else:
                report_data[disease] = 1

        self.env['disease.report'].search([]).unlink()

        for disease_name, count in report_data.items():
            self.env['disease.report'].create({
                'disease_name': disease_name,
                'diagnosis_count': count
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Disease Report',
            'res_model': 'disease.report',
            'view_mode': 'tree',
            'target': 'new',
        }
