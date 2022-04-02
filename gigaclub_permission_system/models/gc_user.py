from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

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
