from odoo import fields, models


class GCDiscordView(models.Model):
    _name = "gc.discord.view"
    _description = "GigaClub Discord View"

    name = fields.Char()
