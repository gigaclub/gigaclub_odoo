from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    azure_client_id = fields.Char(string="Azure Client ID")
    microsoft_login_url = fields.Char(
        string="Microsoft Login URL",
        readonly=True,
        compute="_compute_microsoft_login_url",
        store=True,
    )

    @api.depends("azure_client_id")
    def _compute_microsoft_login_url(self):
        for rec in self.filtered("azure_client_id"):
            rec.microsoft_login_url = f"https://login.live.com/oauth20_authorize.srf?client_id={rec.azure_client_id}&response_type=code&redirect_uri=http://localhost:14069&scope=XboxLive.signin%20offline_access&state=NOT_NEEDED"  # noqa: B950
