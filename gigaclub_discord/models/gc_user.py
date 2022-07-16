from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    discord_name = fields.Char()
    discord_uuid = fields.Char()
    role_ids = fields.Many2many(comodel_name="gc.discord.role")
    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile"
    )

    _sql_constraints = [
        ("discord_uuid_unique", "UNIQUE(discord_uuid)", "DISCORD_UUID must be unique!")
    ]

    @api.depends("discord_name")
    def _compute_name(self):
        super()._compute_name()
        for rec in self.filtered(lambda x: not x.name):
            rec.name = rec.discord_name
