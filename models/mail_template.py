
from odoo import _, api, models
from odoo.tools import pycompat
from odoo.exceptions import UserError
import base64


class MailTemplate(models.Model):
    _inherit = "mail.template"

    @api.multi
    def generate_attachment_email(self, res_ids):
        # When the report document has been already generated it reuses it, othewise it generates it as expected
        self.ensure_one()
        multi_mode = True
        if isinstance(res_ids, pycompat.integer_types):
            res_ids = [res_ids]
            multi_mode = False
        res_ids_to_templates = self.get_email_template(res_ids)
        # templates: res_id -> template; template -> res_ids
        templates_to_res_ids = {}
        for res_id, template in res_ids_to_templates.items():
            templates_to_res_ids.setdefault(template, []).append(res_id)
        results = dict()
        for template, template_res_ids in templates_to_res_ids.items():
            # Add report in attachments: generate once for all template_res_ids
            if template.report_template:
                for res_id in template_res_ids:
                    results[res_id] = {}
                    attachments = []
                    report_name = self._render_template(template.report_name, template.model, res_id)
                    report = template.report_template
                    report_service = report.report_name
                    if report.report_type in ['qweb-html', 'qweb-pdf']:
                        result, format = report.render_qweb_pdf([res_id])
                    else:
                        res = report.render([res_id])
                        if not res:
                            raise UserError(_('Unsupported report type %s found.') % report.report_type)
                        result, format = res
                    result = base64.b64encode(result)
                    if not report_name:
                        report_name = 'report.' + report_service
                    ext = "." + format
                    if not report_name.endswith(ext):
                        report_name += ext
                    attachments.append((report_name, result))
                    results[res_id]['attachments'] = attachments
                    if report.attachment_use and report.model_id:
                        ir_attachments = self.env['ir.attachment'].search([('res_id', '=', res_id), ('res_model', '=', report.model_id.model), ('mimetype', '=', 'application/pdf')])
                        if ir_attachments:
                            if len(ir_attachments) > 1:
                                maybe_old = [attachment_id for attachment_id in ir_attachments if attachment_id.res_model_name == 'Invoice']
                                if maybe_old:
                                    ir_attachment = maybe_old[0]
                                else:
                                    ir_attachment = ir_attachments[0]
                            else:
                                ir_attachment = ir_attachments[0]
                            results[res_id]['reuse_attachments'] = (report_name, ir_attachment.id)
        return multi_mode and results or results[res_ids[0]]
