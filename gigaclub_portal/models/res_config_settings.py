from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    azure_client_id = fields.Char(
        string="Azure Client ID", related="company_id.azure_client_id", readonly=False
    )
    microsoft_login_url = fields.Char(
        string="Microsoft Login URL",
        related="company_id.microsoft_login_url",
        readonly=True,
    )
