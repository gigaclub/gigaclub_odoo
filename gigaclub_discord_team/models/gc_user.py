from odoo import api, models


class GCUser(models.Model):
    _inherit = "gc.user"

    @api.depends("permission_connector_ids.team_id.discord_role_id")
    def _compute_role_ids(self):
        return super()._compute_role_ids()

    def _get_roles(self):
        res = super()._get_roles()
        res |= (
            self.permission_connector_ids.team_id.discord_role_id
            | self.env["gc.team"].search([("owner_id", "=", self.id)]).discord_role_id
        )
        return res
