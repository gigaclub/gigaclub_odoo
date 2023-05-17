from odoo import api, fields, models


class GCMinecraftPlayerStats(models.Model):
    _name = "gc.minecraft.player.stats"
    _description = "GigaClub Minecraft Player Stats"

    user_id = fields.Many2one(comodel_name="gc.user", required=True, index=True)
    server_id = fields.Many2one(comodel_name="gc.minecraft.server", required=True)
    stats_id = fields.Many2one(comodel_name="gc.minecraft.stats", required=True)
    value = fields.Text()

    @api.model
    def register_player_stats(self, data):
        GCUser = self.env["gc.user"]
        GCMinecraftServer = self.env["gc.minecraft.server"]
        GCMinecraftStats = self.env["gc.minecraft.stats"]
        for value in data:
            mc_uuid = value.get("mc_uuid")
            server_name = value.get("server_name")
            stats_name = value.get("stats_name")
            value = value.get("value")
            user = GCUser.search([("mc_uuid", "=", mc_uuid)], limit=1)
            server = GCMinecraftServer.search([("name", "=", server_name)], limit=1)
            if not server:
                server = GCMinecraftServer.create({"name": server_name})
            stat = GCMinecraftStats.search([("name", "=", stats_name)], limit=1)
            user.update_player_stats(server, stat, value)
        return 1
