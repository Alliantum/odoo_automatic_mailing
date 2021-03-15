# -*- encoding: utf-8 -*-

from odoo import models, api, _, SUPERUSER_ID
import base64

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids, template):
        # Here we override to avoid notify about contact assigned to invoices. We don't want it if the customer is already going to receive one automatically
        return

    @api.multi
    def get_email_confirmation_template(self):
        # This is a necessary method because it will decide which report will be used.
        return self.env.ref('odoo_automatic_mailing.automatic_email_template_edi_sale')


    @api.multi
    def action_confirm(self):
        for order in self:
            confirm = super(SaleOrder, order).action_confirm()
            trigger, recipients, message = order.filter_recipients_mailing()
            if trigger:
                template_id = order.get_email_confirmation_template()
                if template_id:
                    for contact in recipients:
                        post_params = dict(
                            template_id=template_id.id,
                            message_type='comment',
                            subtype_id=self.env['ir.model.data'].xmlid_to_res_id('odoo_automatic_mailing.mt_automatic_mailing'),
                            notif_layout='mail.mail_notification_paynow',
                            attachment_ids=[],
                            partner_ids=[(6, False, [contact.id])],
                            )
                        order.sudo(SUPERUSER_ID).with_context(lang=contact.lang, body_to_lang=contact.lang or 'en_US').message_post_with_template(**post_params)
            if message:
                odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
                channel_id = self.sudo(self.env.user.id).env['mail.channel'].search([('name', '=', 'OdooBot')], limit=1)
                if not channel_id:
                    channel_id = self.env['mail.channel'].with_context({"mail_create_nosubscribe": True}).create({
                        'channel_partner_ids': [(4, self.env.user.id), (4, odoobot_id)],
                        'public': 'private',
                        'channel_type': 'chat',
                        'email_send': False,
                        'name': 'OdooBot'
                    })
                channel_id.sudo().message_post(body=message, author_id=odoobot_id, message_type="comment",
                                            subtype="mail.mt_comment")
            return confirm
