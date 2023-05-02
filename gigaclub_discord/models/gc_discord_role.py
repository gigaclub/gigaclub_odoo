from odoo import api, fields, models


class GCDiscordRole(models.Model):
    _name = "gc.discord.role"
    _description = "GigaClub Discord Role"

    name = fields.Char()
    role_id = fields.Char()
    hoist = fields.Boolean()
    mentionable = fields.Boolean()
    color = fields.Char(default="#FFFFFF")

    user_ids = fields.Many2many(comodel_name="gc.user", compute="_compute_user_ids")
    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile"
    )
    permission_group_id = fields.Many2one(
        comodel_name="gc.permission.group", index=True
    )

    @api.depends("permission_group_id")
    def _compute_user_ids(self):
        for rec in self:
            rec.user_ids = rec.permission_group_id.user_ids
