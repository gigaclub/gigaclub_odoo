from odoo import fields, models


class GCPermissionProfileEntry(models.Model):
    _name = "gc.permission.profile.entry"
    _inherits = {
        "gc.permission.profile.entry.template": "permission_profile_entry_template_id"
    }
    _description = "GigaClub Permission Profile Entry"

    permission_profile_id = fields.Many2one(
        comodel_name="gc.permission.profile", required=True, index=True
    )
    permission_profile_entry_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.entry.template", required=True
    )
