from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    language_id = fields.Many2one(
        comodel_name="gc.language",
        default=lambda x: x.env["gc.language"].search([("default", "=", True)]),
    )

    @api.model
    def set_language(self, player_uuid, language):
        user_id = self.search([("mc_uuid", "=", player_uuid)])
        language_id = self.env["gc.language"].search([("name", "=ilike", language)])
        if len(user_id) > 0 and len(language_id) > 0:
            user_id.language_id = language_id
            return True
        return False
