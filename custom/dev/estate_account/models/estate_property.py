from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_status_sold(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': 'Property Sale: %s' % self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        })
        return super().action_set_status_sold()