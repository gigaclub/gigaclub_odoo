from odoo import fields, models


class GCDiscordTextInput(models.Model):
    _name = "gc.discord.text.input"
    _inherit = "gc.discord.item"
    _description = "GigaClub Discord Text Input"

    name = fields.Char()
