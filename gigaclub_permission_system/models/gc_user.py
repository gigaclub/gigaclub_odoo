from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    permission_connector_ids = fields.One2many(
        comodel_name="gc.permission.connector", inverse_name="user_id", index=True
    )

    permission_group_ids = fields.Many2many(comodel_name="gc.permission.group")
    permission_profile_ids = fields.Many2many(comodel_name="gc.permission.profile")

    def get_permissions(self):
        self.ensure_one()
        permission_model_entries = (
            self.permission_group_ids.mapped(
                "permission_profile_ids.permission_profile_entry_template_ids.permission_model_entry_id"  # noqa: B950
            )
            | self.permission_profile_ids.mapped(
                "permission_profile_entry_template_ids.permission_model_entry_id"
            )
        ).filtered(lambda x: x.permission_type == "user")
        return permission_model_entries

    def has_permission(self, permission):
        self.ensure_one()
        return (
            self.env["gc.permission.model.entry"].search(
                [("name", "=ilike", permission)], limit=1
            )
            in self.get_permissions()
        )

    def has_one_of_permissions(self, permissions):
        self.ensure_one()
        return any(
            self.env["gc.permission.model.entry"].search(
                [("name", "=ilike", permission)], limit=1
            )
            in self.get_permissions()
            for permission in permissions
        )
