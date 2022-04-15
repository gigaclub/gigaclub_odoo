from odoo import fields, models


class GCPermissionConnector(models.Model):
    _inherit = "gc.permission.connector"

    world_ids = fields.Many2many(comodel_name="gc.builder.world")
