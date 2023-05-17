from odoo import fields, models


class GCMinecraftServer(models.Model):
    _name = "gc.minecraft.server"
    _description = "GigaClub Minecraft Server"

    name = fields.Char(required=True)

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]
