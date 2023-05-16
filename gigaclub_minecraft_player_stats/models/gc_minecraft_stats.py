from odoo import fields, models


class GCMinecraftStats(models.Model):
    _name = "gc.minecraft.stats"
    _description = "GigaClub Minecraft Stats"

    name = fields.Char()
    ttype = fields.Selection(...)
