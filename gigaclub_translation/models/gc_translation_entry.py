from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class GCTranslationEntry(models.Model):
    _name = "gc.translation.entry"
    _description = "GigaClub Translation Entry"

    @api.model
    def _get_languages(self):
        return self.env["res.lang"].get_installed()

    minecraft_tellraw_line_ids = fields.One2many(
        comodel_name="minecraft.tellraw.line", inverse_name="translation_entry_id"
    )
    widgets = fields.Serialized(compute="_compute_widgets", store=True)
    translation_ids = fields.Many2many(comodel_name="gc.translation")
    lang = fields.Selection(selection=_get_languages, required=True)

    # inverse for entry_ids in gc.language
    translation_id = fields.Many2one(comodel_name="gc.translation")

    @api.depends("translation_ids.values")
    def _compute_widgets(self):
        for rec in self:
            values = rec.translation_ids.mapped("values")
            widgets = {"params": [], "list": []}
            for value in values:
                try:
                    value = safe_eval(value)
                except Exception:
                    value = {}
                if "params" in value and value["params"]:
                    widgets["params"].extend(list(value["params"].keys()))
                if "list" in value and value["list"]:
                    widgets["list"].extend(list(value["list"].keys()))
            rec.widgets = widgets
