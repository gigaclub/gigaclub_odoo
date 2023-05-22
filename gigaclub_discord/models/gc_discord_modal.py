from odoo import fields, models


class GCDiscordModal(models.Model):
    _name = "gc.discord.modal"
    _description = "GigaClub Discord Modal"

    title = fields.Char()
