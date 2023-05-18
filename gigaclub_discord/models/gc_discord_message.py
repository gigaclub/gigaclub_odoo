from odoo import fields, models


class GCDiscordMessage(models.Model):
    _name = "gc.discord.message"
    _description = "GigaClub Discord Message"

    name = fields.Char()
    channel_id = fields.Many2one(comodel_name="gc.discord.channel")
