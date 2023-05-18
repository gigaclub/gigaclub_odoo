from odoo import fields, models


class GCTeam(models.Model):
    _inherit = "gc.team"

    should_have_discord_channel = fields.Boolean()
    discord_category_id = fields.Many2one(comodel_name="gc.discord.category")
    discord_role_id = fields.Many2one(comodel_name="gc.discord.role")

    def update_team_channels(self):
        self.ensure_one()
        if not self.should_have_discord_channel:
            self.discord_category_id.unlink()
            self.discord_role_id.unlink()
            return
        if not self.discord_category_id:
            self.discord_category_id = self.env["gc.discord.category"].create(
                {
                    "name": self.name,
                    "channel_ids": [
                        (0, 0, {"name": f"{self.name} text channel", "type": "text"}),
                        (0, 0, {"name": f"{self.name} voice channel", "type": "voice"}),
                    ],
                }
            )
            self.discord_role_id = self.env["gc.discord.role"].create(
                {
                    "name": self.name,
                }
            )
            everyone_role = self.env.ref("gigaclub_discord.gc_discord_role_everyone")
            self.discord_category_id.overwrite_permission_profile_ids = [
                (
                    0,
                    0,
                    {
                        "category_id": self.discord_category_id.id,
                        "overwrite_entity_id": f"gc.discord.role,{everyone_role.id}",
                        "permission_profile_id": self.env[
                            "gc.discord.permission.profile"
                        ]
                        .create(
                            {
                                "read_messages": False,
                            }
                        )
                        .id,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "category_id": self.discord_category_id.id,
                        "overwrite_entity_id": f"gc.discord.role,{self.discord_role_id.id}",
                        "permission_profile_id": self.env[
                            "gc.discord.permission.profile"
                        ]
                        .create(
                            {
                                "read_messages": True,
                            }
                        )
                        .id,
                    },
                ),
            ]
            return
        self.discord_category_id.name = self.name
        for channel in self.discord_category_id.channel_ids:
            channel.name = f"{self.name} {channel.type} channel"
