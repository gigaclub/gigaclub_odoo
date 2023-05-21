from odoo import fields, models


class GCReward(models.Model):
    _inherit = "gc.reward"

    permission_group_ids = fields.Many2many(comodel_name="gc.permission.group")
