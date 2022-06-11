from odoo import api, fields, models


class GCPermissionGroup(models.Model):
    _name = "gc.permission.group"
    _description = "GigaClub Permission Group"

    name = fields.Char()
    description = fields.Text()
    permission_profile_ids = fields.One2many(
        comodel_name="gc.permission.profile", inverse_name="permission_group_id"
    )
    global_group = fields.Boolean()

    parent_group_id = fields.Many2one(comodel_name="gc.permission.group", index=True)
    child_group_ids = fields.One2many(
        comodel_name="gc.permission.group", inverse_name="parent_group_id"
    )

    computed_permission_profile_ids = fields.Many2many(
        comodel_name="gc.permission.profile", compute="_compute_permissions"
    )

    @api.depends(
        "child_group_ids.computed_permission_profile_ids", "permission_profile_ids"
    )
    def _compute_permissions(self):
        for rec in self:
            rec.computed_permission_profile_ids = (
                rec.child_group_ids.mapped("computed_permission_profile_ids")
                | rec.permission_profile_ids
            )

    @api.model
    def get_all_groups(self):
        return self._get_groups(self.search([("global_group", "=", True)]))

    @api.model
    def set_groups(self, playerUUID, group_ids):
        user = self.env["gc.user"].search([("mc_uuid", "=", playerUUID)], limit=1)
        groups = self.browse(group_ids)
        user.permission_group_ids |= groups
        return 0

    @api.model
    def remove_groups(self, playerUUID, group_ids):
        user = self.env["gc.user"].search([("mc_uuid", "=", playerUUID)], limit=1)
        groups = self.browse(group_ids)
        user.permission_group_ids -= groups
        return 0

    @api.model
    def get_groups(self, playerUUID):
        user = self.env["gc.user"].search([("mc_uuid", "=", playerUUID)], limit=1)
        return self._get_groups(user.permission_group_ids)

    def _get_groups(self, records):
        return [
            {
                "id": x.id,
                "name": x.name,
                "description": x.description,
                "permissions": x.computed_permission_profile_ids.mapped(
                    "permission_profile_entry_ids.permission_model_entry_id.name"
                ),
            }
            for x in records
        ]
