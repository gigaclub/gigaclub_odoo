from odoo import fields, models


class GCPermissionMixin(models.AbstractModel):
    _name = "gc.permission.mixin"
    _description = "GigaClub Permission Mixin"

    permission_group_ids = fields.Many2many(comodel_name="gc.permission.group")
    permission_profile_ids = fields.Many2many(comodel_name="gc.permission.profile")

    def get_permissions(self):
        self.ensure_one()
        permission_model_entries = self.permission_group_ids.mapped(
            "permission_profile_ids.permission_model_ids.permission_model_entry_ids"
        ) | self.permission_profile_ids.mapped(
            "permission_model_ids.permission_model_entry_ids"
        )
        return permission_model_entries

    def has_permission(self, permission):
        self.ensure_one()
        return permission in self.get_permissions()
