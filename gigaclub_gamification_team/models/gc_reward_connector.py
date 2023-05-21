from odoo import fields, models


class GCRewardConnector(models.Model):
    _inherit = "gc.reward.connector"

    team_id = fields.Many2one(comodel_name="gc.team")
