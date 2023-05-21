from odoo import fields, models


class GCRewardConnector(models.Model):
    _name = "gc.reward.connector"
    _description = "GigaClub Reward Connector"

    reward_id = fields.Many2one(comodel_name="gc.reward")
    user_id = fields.Many2one(comodel_name="gc.user")
