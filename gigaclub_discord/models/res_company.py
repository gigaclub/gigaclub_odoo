from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    discord_server_id = fields.Char(string="Discord Server ID")
    discord_server_status = fields.Selection(
        selection=[
            ("started", "Started"),
            ("stopped", "Stopped"),
        ],
        default="stopped",
    )
    discord_server_rules = fields.Text()
