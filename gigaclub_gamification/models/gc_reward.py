from odoo import fields, models


class GCReward(models.Model):
    _name = "gc.reward"
    _description = "GigaClub Reward"

    name = fields.Char()
    coins = fields.Integer()
    experience_points = fields.Integer()
