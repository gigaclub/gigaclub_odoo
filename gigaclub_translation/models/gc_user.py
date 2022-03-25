from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    language_id = fields.Many2one(
        comodel_name="gc.language",
        default=lambda x: x.env["gc.language"].search([("default", "=", True)]),
    )

    @api.model
    def set_language(self, player_uuid, language):
        user = self.search([("mc_uuid", "=", player_uuid)])
        language = self.env["gc.language"].search([("name", "=ilike", language)])
        if user and language:
            user.language_id = language
            return True
        return False
