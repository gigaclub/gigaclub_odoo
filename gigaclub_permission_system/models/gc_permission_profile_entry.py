from odoo import fields, models


class GCPermissionProfileEntry(models.Model):
    _name = "gc.permission.profile.entry"
    _description = "GigaClub Permission Profile Entry"

    permission_profile_id = fields.Many2one(
        comodel_name="gc.permission.profile", required=True
    )
    permission_model_entry_id = fields.Many2one(
        comodel_name="gc.permission.model.entry", required=True
    )
    allowed = fields.Boolean()
