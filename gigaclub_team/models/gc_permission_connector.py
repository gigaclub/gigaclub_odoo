from odoo import fields, models


class GCPermissionConnector(models.Model):
    _inherit = "gc.permission.connector"

    team_ids = fields.Many2many(comodel_name="gc.team")
