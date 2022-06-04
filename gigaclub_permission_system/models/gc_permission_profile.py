from odoo import fields, models


class GCPermissionProfile(models.Model):
    _name = "gc.permission.profile"
    _inherits = {"gc.permission.profile.template": "permission_profile_template_id"}
    _description = "GigaClub Permission Profile"

    permission_profile_entry_ids = fields.One2many(
        comodel_name="gc.permission.profile.entry", inverse_name="permission_profile_id"
    )
    permission_profile_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.template", required=True
    )
    permission_group_id = fields.Many2one(
        comodel_name="gc.permission.group", index=True
    )
