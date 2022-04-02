from odoo import fields, models


class GCPermissionProfile(models.Model):
    _name = "gc.permission.profile"
    _description = "GigaClub Permission Profile"

    permission_model_ids = fields.Many2many(comodel_name="gc.permission.model")
