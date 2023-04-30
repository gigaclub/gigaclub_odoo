from odoo import fields, models


class GCDiscordRole(models.Model):
    _name = "gc.discord.role"
    _description = "GigaClub Discord Role"

    name = fields.Char()
    role_id = fields.Char()
    hoist = fields.Boolean()
    position = fields.Integer()
    mentionable = fields.Boolean()
    color = fields.Char()

    user_ids = fields.Many2many(comodel_name="gc.user")
    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile"
    )
