# -*- encoding: utf-8 -*-

from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.users"

    # Boolean field to know if this user should receive an automated mail
    os_enable_email_receivable = fields.Boolean('Enable Mail receivable', help="Automatic mailing on Sale's Order confirmation")

