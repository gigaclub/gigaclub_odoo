from odoo import fields, models


class GCTeam(models.Model):
    _inherit = "gc.team"

    should_have_discord_channel = fields.Boolean()
    discord_category_id = fields.Many2one(comodel_name="gc.discord.category")

    def update_team_channels(self):
        self.ensure_one()
        if not self.should_have_discord_channel:
            self.discord_category_id.unlink()
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
            return
        self.discord_category_id.name = self.name
        for channel in self.discord_category_id.channel_ids:
            channel.name = f"{self.name} {channel.type} channel"
