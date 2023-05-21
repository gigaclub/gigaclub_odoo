from odoo import fields, models


class GCAdvancement(models.Model):
    _name = "gc.advancement"
    _description = "GigaClub Advancement"

    name = fields.Char()
    description = fields.Text()
    reward_ids = fields.Many2many(comodel_name="gc.reward")
