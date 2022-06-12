from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    @api.model
    def _get_languages(self):
        return self.env["res.lang"].get_installed()

    lang = fields.Selection(selection=_get_languages, required=True)

    @api.model
    def set_language(self, player_uuid, lang_code):
        user = self.search([("mc_uuid", "=", player_uuid)])
        if user and lang_code:
            try:
                user.lang = lang_code
                return True
            except Exception:
                pass
        return False

    @api.model
    def get_language(self, player_uuid):
        user = self.search([("mc_uuid", "=", player_uuid)])
        if user:
            return user.lang
        return False
