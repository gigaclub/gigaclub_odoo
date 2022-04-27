from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    permission_connector_ids = fields.One2many(
        comodel_name="gc.permission.connector", inverse_name="user_id", index=True
    )
