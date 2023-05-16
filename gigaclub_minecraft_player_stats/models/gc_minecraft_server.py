from odoo import fields, models


class GCMinecraftServer(models.Model):
    _name = "gc.minecraft.server"
    _description = "GigaClub Minecraft Server"

    name = fields.Char()
