from odoo import fields, models


class GCDiscordSelect(models.Model):
    _name = "gc.discord.select"
    _inherit = "gc.discord.item"
    _description = "GigaClub Discord Select"

    name = fields.Char()
    select_item_ids = fields.One2many(
        comodel_name="gc.discord.select.item", inverse_name="select_id"
    )
