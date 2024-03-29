from odoo import api, fields, models


class GCPermissionGroup(models.Model):
    _name = "gc.permission.group"
    _description = "GigaClub Permission Group"

    prefix = fields.Char()
    name = fields.Char()
    suffix = fields.Char()
    display = fields.Char()
    color = fields.Char()
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
        comodel_name="gc.permission.profile",
        compute="_compute_permissions",
        recursive=True,
    )
    user_ids = fields.Many2many(comodel_name="gc.user")

    @api.depends(
        "child_group_ids.computed_permission_profile_ids", "permission_profile_ids"
    )
    def _compute_permissions(self):
        for rec in self:
            rec.computed_permission_profile_ids = (
                rec.parent_group_id.computed_permission_profile_ids
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
                "prefix": x.prefix or "",
                "name": x.name or "",
                "suffix": x.suffix or "",
                "display": x.display or "",
                "color": x.color or "",
                "description": x.description or "",
                "permissions": x.computed_permission_profile_ids.mapped(
                    "permission_profile_entry_ids.permission_model_entry_id.name"
                ),
            }
            for x in records
        ]
