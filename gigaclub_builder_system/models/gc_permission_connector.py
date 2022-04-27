from odoo import fields, models


class GCPermissionConnector(models.Model):
    _inherit = "gc.permission.connector"

    world_id = fields.Many2one(comodel_name="gc.builder.world")
