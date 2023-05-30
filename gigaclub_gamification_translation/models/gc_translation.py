from odoo import fields, models


class GCTranslation(models.Model):
    _inherit = "gc.translation"

    reward_id = fields.Many2one(comodel_name="gc.reward")
