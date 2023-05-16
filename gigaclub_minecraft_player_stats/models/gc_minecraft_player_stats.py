from odoo import fields, models


class GCMinecraftPlayerStats(models.Model):
    _name = "gc.minecraft.player.stats"
    _description = "GigaClub Minecraft Player Stats"

    user_id = fields.Many2one(comodel_name="gc.user", required=True, index=True)
    server_id = fields.Many2one(comodel_name="gc.minecraft.server", required=True)
    stats_id = fields.Many2one(comodel_name="gc.minecraft.stats", required=True)
    value = fields.Text()
