from odoo import fields, models


class GCDiscordPermissionProfileOverwrite(models.Model):
    _name = "gc.discord.permission.profile.overwrite"
    _description = "GigaClub Discord Permission Profile overwrite"

    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile", required=True
    )
    overwrite_entity_id = fields.Reference(
        selection=[("gc.discord.role", "gc.discord.role"), ("gc.user", "gc.user")],
        required=True,
    )

    channel_id = fields.Many2one(comodel_name="gc.discord.channel", index=True)
    category_id = fields.Many2one(comodel_name="gc.discord.category", index=True)
