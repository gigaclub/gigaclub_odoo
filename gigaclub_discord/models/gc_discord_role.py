from odoo import fields, models


class GCDiscordRole(models.Model):
    _name = "gc.discord.role"
    _description = "GigaClub Discord Role"

    name = fields.Char()
    role_id = fields.Char()
    hoist = fields.Boolean()
    position = fields.Integer(default=1, required=True)
    mentionable = fields.Boolean()
    color = fields.Char(default="#FFFFFF")

    user_ids = fields.Many2many(comodel_name="gc.user")
    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile"
    )
