from odoo import fields, models


class GCDiscordItem(models.AbstractModel):
    _name = "gc.discord.item"
    _description = "GigaClub Discord Item"

    view_id = fields.Many2one(comodel_name="gc.discord.view")
    custom_id = fields.Char()
