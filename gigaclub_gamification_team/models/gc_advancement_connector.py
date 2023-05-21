from odoo import fields, models


class GCAdvancementConnector(models.Model):
    _inherit = "gc.advancement.connector"

    team_id = fields.Many2one(comodel_name="gc.team")
