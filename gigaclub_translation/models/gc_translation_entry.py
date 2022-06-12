from odoo import api, fields, models


class GCTranslationEntry(models.Model):
    _name = "gc.translation.entry"
    _description = "GigaClub Translation Entry"

    @api.model
    def _get_languages(self):
        return self.env["res.lang"].get_installed()

    content = fields.Text(required=True)
    translation_ids = fields.Many2many(comodel_name="gc.translation")
    lang = fields.Selection(selection=_get_languages, required=True)

    # inverse for entry_ids in gc.language
    translation_id = fields.Many2one(comodel_name="gc.translation")
