from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'


    invoice_automatic_template_id = fields.Many2one('mail.template', default=lambda self: self.env.ref('odoo_automatic_mailing.automatic_email_template_edi_invoice').id)
    sale_automatic_template_id = fields.Many2one('mail.template', default=lambda self: self.env.ref('odoo_automatic_mailing.automatic_email_template_edi_sale').id)
