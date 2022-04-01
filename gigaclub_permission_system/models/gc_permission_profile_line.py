from odoo import fields, models


class GCPermissionProfileLine(models.Model):
    _name = "gc.permission.profile.line"
    _description = "GigaClub Permission Profile Line"

    permission_profile_id = fields.Many2one(
        comodel_name="gc.permission.profile", required=True
    )
    permission_group_id = fields.Many2one(
        comodel_name="gc.permission.group", required=True
    )
