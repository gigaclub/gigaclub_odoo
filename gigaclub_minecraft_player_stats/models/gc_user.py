from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    player_stats_ids = fields.One2many(
        comodel_name="gc.minecraft.player.stats", inverse_name="user_id"
    )
