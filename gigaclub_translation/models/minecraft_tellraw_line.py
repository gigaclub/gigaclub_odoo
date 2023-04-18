from odoo import fields, models


class MinecraftTellrawLine(models.Model):
    _inherit = "minecraft.tellraw.line"

    translation_entry_id = fields.Many2one(comodel_name="gc.translation.entry")
