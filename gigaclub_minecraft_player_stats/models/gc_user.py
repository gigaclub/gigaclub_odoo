from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    player_stats_ids = fields.One2many(
        comodel_name="gc.minecraft.player.stats", inverse_name="user_id"
    )

    def update_player_stats(self, server, stat, value):
        self.ensure_one()
        player_stat = self.env["gc.minecraft.player.stats"].search(
            [("server_id", "=", server.id), ("stats_id", "=", stat.id)], limit=1
        )
        if not player_stat:
            self.env["gc.minecraft.player.stats"].create(
                {"server_id": server.id, "stats_id": stat.id, "value": value}
            )
        else:
            player_stat.write({"value": value})
