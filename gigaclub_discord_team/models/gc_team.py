from odoo import api, models


class GCTeam(models.Model):
    _inherit = "gc.team"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.create_team_channels()
        return records

    def create_team_channels(self):
        self.ensure_one()
        self.env["gc.discord.category"].create(
            {
                "name": self.name,
                "channel_ids": [
                    (0, 0, {"name": f"{self.name} text channel", "type": "text"}),
                    (0, 0, {"name": f"{self.name} voice channel", "type": "voice"}),
                ],
            }
        )
