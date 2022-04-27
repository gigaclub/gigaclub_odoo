from odoo import fields, models


class GCPermissionConnector(models.Model):
    _inherit = "gc.permission.connector"

    team_id = fields.Many2one(comodel_name="gc.team")
