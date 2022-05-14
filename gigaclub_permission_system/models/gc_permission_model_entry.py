from odoo import fields, models


class GCPermissionModelEntry(models.Model):
    _name = "gc.permission.model.entry"
    _description = "GigaClub Permission Model Entry"

    permission_model_id = fields.Many2one(
        comodel_name="gc.permission.model", required=True, index=True
    )
    name = fields.Char(required=True, index=True)
    permission_type = fields.Selection(
        selection=[("connector", "Connector"), ("user", "User")], required=True
    )
