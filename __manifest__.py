# -*- coding: utf-8 -*-
{
    'name': "Automatic Mailing",
    'summary': """
        SO and Invoices automatic mailing on Confirmation""",
    'description': """
        Sends email automatically in Sale Orders and Invoices after being confirmed or validated.

        - New field added in Contact form, under tab Invoicing/Invoicing Channel. When set to 'Email'
        the automated emails will be sent for that contact. If not manually set during contact creation, its value defaults
        to 'Email'.
    """,
    'author': "Alliantum",
    'website': "https://www.alliantum.com",
    'category': 'Technical Settings',
    'version': '12.0.1.0.0',
    'depends': ['base', 'sale', 'account', 'purchase', 'mail', 'odoo_invoice_addresses'],
    'data': [
        'views/res_partner_form.xml',
        'views/res_users_form.xml',
        'data/sale_automatic_template.xml',
        'data/invoice_automatic_template.xml',
        'data/subtype.xml',
    ],
}
