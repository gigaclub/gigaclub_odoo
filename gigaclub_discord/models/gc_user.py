from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    discord_uuid = fields.Char()
    role_ids = fields.Many2many(
        comodel_name="gc.discord.role", compute="_compute_role_ids"
    )

    _sql_constraints = [
        ("discord_uuid_unique", "UNIQUE(discord_uuid)", "DISCORD_UUID must be unique!")
    ]

    @api.depends("permission_group_ids.role_ids")
    def _compute_role_ids(self):
        for rec in self:
            rec.role_ids = rec._get_roles()

    def _get_roles(self):
        self.ensure_one()
        return self.permission_group_ids.role_ids
