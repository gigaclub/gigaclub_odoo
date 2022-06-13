from odoo import api, fields, models


class GCPermissionConnector(models.Model):
    _inherit = "gc.permission.connector"

    world_id = fields.Many2one(comodel_name="gc.builder.world", index=True)

    @api.model
    def get_team_worlds(self, team_id):
        return [
            self.env["gc.builder.world"].return_world(x)
            for x in self.search([("team_id", "=", team_id)]).mapped("world_id")
        ]

    @api.model
    def get_user_worlds(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if user:
            return [
                self.env["gc.builder.world"].return_world(x)
                for x in self.search([("user_id", "=", user.id)]).mapped("world_id")
            ]
        return []
