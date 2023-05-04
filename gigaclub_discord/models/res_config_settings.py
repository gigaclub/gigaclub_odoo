from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    discord_server_id = fields.Char(
        related="company_id.discord_server_id", readonly=False
    )
    discord_server_status = fields.Selection(related="company_id.discord_server_status")
    discord_server_rules = fields.Text(
        related="company_id.discord_server_rules", readonly=False
    )

    def start_discord_bot(self):
        return {
            "name": "start",
            "res_model": "ir.actions.act_url",
            "type": "ir.actions.act_url",
            "target": "_blank",
            "url": "/discordbot/start",
        }

    def stop_discord_bot(self):
        return {
            "name": "stop",
            "res_model": "ir.actions.act_url",
            "type": "ir.actions.act_url",
            "target": "_blank",
            "url": "/discordbot/stop",
        }

    def reload_discord_bot(self):
        return {
            "name": "reload",
            "res_model": "ir.actions.act_url",
            "type": "ir.actions.act_url",
            "target": "_blank",
            "url": "/discordbot/reload",
        }
