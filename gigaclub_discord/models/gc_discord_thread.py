from odoo import fields, models


class GCDiscordThread(models.Model):
    _name = "gc.discord.thread"
    _description = "GigaClub Discord Thread"

    name = fields.Char()
    user_ids = fields.Many2many(comodel_name="gc.user")
