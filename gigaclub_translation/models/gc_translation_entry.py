from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class GCTranslationEntry(models.Model):
    _name = "gc.translation.entry"
    _description = "GigaClub Translation Entry"

    @api.model
    def _get_languages(self):
        return self.env["res.lang"].get_installed()

    content = fields.Text()
    widgets = fields.Text(compute="_compute_widgets")
    translation_ids = fields.Many2many(comodel_name="gc.translation")
    lang = fields.Selection(selection=_get_languages, required=True)

    # inverse for entry_ids in gc.language
    translation_id = fields.Many2one(comodel_name="gc.translation")

    @api.depends("translation_ids.values")
    def _compute_widgets(self):
        for rec in self:
            values = rec.translation_ids.mapped("values")
            widgets = ""
            for value in values:
                try:
                    value = safe_eval(value)
                except Exception:
                    value = {}
                for key, val in value.items():
                    widgets += f"<{key}>: {val}\n"
            rec.widgets = widgets
