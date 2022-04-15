from odoo import fields, models


class GCUser(models.Model):
    _name = "gc.user"

    permission_connector_ids = fields.Many2many(comodel_name="gc.permission.connector")
