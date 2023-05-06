import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class GCUser(models.Model):
    _inherit = "gc.user"

    # grepper odoo get installed languages
    @api.model
    def _get_languages(self):
        return self.env["res.lang"].get_installed()

    # end grepper

    lang = fields.Selection(selection=_get_languages, required=True)

    @api.model
    def set_language(self, player_uuid, lang_code):
        user = self.search([("mc_uuid", "=", player_uuid)])
        if user and lang_code:
            try:
                user.lang = lang_code
                return True
            except Exception:
                _logger.exception("Error when setting lang:")
        return False

    @api.model
    def get_language(self, player_uuid):
        user = self.search([("mc_uuid", "=", player_uuid)])
        if user:
            return user.lang
        return False
