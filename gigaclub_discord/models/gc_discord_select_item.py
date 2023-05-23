from odoo import fields, models


class GCDiscordSelectItem(models.Model):
    _name = "gc.discord.select.item"
    _description = "GigaClub Discord Select Item"

    name = fields.Char()
    select_id = fields.Many2one(comodel_name="gc.discord.select", index=True)
