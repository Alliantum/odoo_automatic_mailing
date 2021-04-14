from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'


    # invoice_automatic_template_id = fields.Many2one('mail.template', default=lambda self: self.env.ref('odoo_automatic_mailing.automatic_email_template_edi_invoice', raise_if_not_found=False))
    # sale_automatic_template_id = fields.Many2one('mail.template', default=lambda self: self.env.ref('odoo_automatic_mailing.automatic_email_template_edi_sale', raise_if_not_found=False))
    automatic_mailing_rule_ids = fields.One2many(comodel_name='automatic.mailing.rule', inverse_name='company_id')
