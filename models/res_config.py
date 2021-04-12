from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_automatic_template_id = fields.Many2one(related='company_id.invoice_automatic_template_id', string="Invoicing Automatic Mail", readonly=False)
    sale_automatic_template_id = fields.Many2one(related='company_id.sale_automatic_template_id', string="Sale Automatic Mail", readonly=False)
