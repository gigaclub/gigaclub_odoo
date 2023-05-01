from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    discord_server_id = fields.Char("Discord Server ID")
    discord_system_channel_id = fields.Many2one(comodel_name="gc.discord.channel")
    discord_server_status = fields.Selection(
        [
            ("started", "Started"),
            ("stopped", "Stopped"),
        ],
        default="stopped",
    )
