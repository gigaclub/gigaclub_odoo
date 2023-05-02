from odoo import fields, models


class GCPermissionModelEntry(models.Model):
    _name = "gc.permission.model.entry"
    _description = "GigaClub Permission Model Entry"

    permission_model_id = fields.Many2one(
        comodel_name="gc.permission.model", index=True, ondelete="cascade"
    )
    nice_name = fields.Char(
        translate=True
    )  # TODO: add nice name to all model entries and use them for Portal display
    name = fields.Char(required=True, index=True)
    permission_type = fields.Selection(
        selection=[("connector", "Connector"), ("user", "User")], required=True
    )
