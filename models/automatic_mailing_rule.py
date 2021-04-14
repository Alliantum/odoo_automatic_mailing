from odoo import _, api, fields, models


class AutomaticMailingRule(models.Model):
    _name = 'automatic.mailing.rule'
    _description = 'Automatic Mailing Rule'

    sequence = fields.Integer()
    company_id = fields.Many2one('res.company', required=True, ondelete="cascade")
    model_id = fields.Many2one('ir.model', string='Apply On', required=True, ondelete="cascade", domain="[('model', 'in', ['sale.order', 'account.invoice'])]")
    model_name = fields.Char(related="model_id.model")
    filter_model_id = fields.Char(string="Apply On", help="Extended filtering option to trigger the line for this model.")
    template_id = fields.Many2one('mail.template', string="Mail Template", required=True)
