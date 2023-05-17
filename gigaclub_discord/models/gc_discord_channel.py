from odoo import fields, models


class GCDiscordChannel(models.Model):
    _name = "gc.discord.channel"
    _description = "GigaClub Discord Channel"

    name = fields.Char(translate=True, required=True)
    discord_channel_uuid = fields.Char(readonly=True)
    type = fields.Selection(
        selection=[
            ("text", "Text"),
            ("voice", "Voice"),
            ("stage", "Stage"),
            ("announcement", "Announcement"),
        ],
        required=True,
    )
    category_id = fields.Many2one(
        comodel_name="gc.discord.category", ondelete="cascade"
    )
    permission_profile_id = fields.Many2one(
        comodel_name="gc.discord.permission.profile"
    )
