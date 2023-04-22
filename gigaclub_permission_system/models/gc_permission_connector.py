from odoo import fields, models


class GCPermissionConnector(models.Model):
    _name = "gc.permission.connector"
    _description = "GigaClub Permission Connector"

    user_id = fields.Many2one(comodel_name="gc.user", ondelete="cascade")

    permission_group_ids = fields.Many2many(comodel_name="gc.permission.group")
    permission_profile_ids = fields.Many2many(comodel_name="gc.permission.profile")

    def get_permissions(self):
        self.ensure_one()
        # TODO: check if this can be simplified
        permission_model_entries = (
            self.permission_group_ids.mapped(
                "permission_profile_ids.permission_profile_entry_template_ids.permission_model_entry_id"  # noqa: B950
            )
            | self.permission_group_ids.mapped(
                "permission_profile_ids.permission_profile_entry_ids.permission_model_entry_id"  # noqa: B950
            )
            | self.permission_profile_ids.mapped(
                "permission_profile_entry_template_ids.permission_model_entry_id"
            )
            | self.permission_profile_ids.mapped(
                "permission_profile_entry_ids.permission_model_entry_id"
            )
        ).filtered(lambda x: x.permission_type == "connector")
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
