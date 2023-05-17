from typing import List

from odoo import api, fields, models


class GCMinecraftStats(models.Model):
    _name = "gc.minecraft.stats"
    _description = "GigaClub Minecraft Stats"

    name = fields.Char(required=True)
    ttype = fields.Selection(selection=[("ticks", "Ticks")])
    active = fields.Boolean(default=True)

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]

    @api.model
    def get_minecraft_stats_types(self) -> List[str]:
        return [x.name for x in self.search([])]
