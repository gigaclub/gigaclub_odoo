from odoo import fields, models


class GCDiscordView(models.Model):
    _name = "gc.discord.view"
    _description = "GigaClub Discord View"

    name = fields.Char()
    button_ids = fields.One2many(
        comodel_name="gc.discord.button", inverse_name="view_id"
    )
    select_ids = fields.One2many(
        comodel_name="gc.discord.select", inverse_name="view_id"
    )
