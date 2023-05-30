from odoo import fields, models


class GCDiscordButton(models.Model):
    _name = "gc.discord.button"
    _inherit = "gc.discord.item"
    _description = "GigaClub Discord Item"

    name = fields.Char()
