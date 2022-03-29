import json
import uuid

import requests

from odoo import _, tools
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


class GigaClubPortal(CustomerPortal):
    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in ["name", "email"]:
            if not data.get(field_name):
                error[field_name] = "missing"

        # email validation
        if data.get("email") and not tools.single_email_re.match(data.get("email")):
            error["email"] = "error"
            error_message.append(
                _("Invalid Email! Please enter a valid email address.")
            )

        # error message for empty required fields
        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        return error, error_message

    @route(["/my/account/save"], type="http", auth="user", website=True)
    def my_account_save(self, **post_values):
        partner = request.env.user.partner_id
        values = {
            "error": {},
            "error_message": [],
        }
        error, error_message = self.details_form_validate(post_values)
        values.update({"error": error, "error_message": error_message})
        values.update(post_values)
        if not error:
            form_values = {}
            for field in ["name", "email"]:
                try:
                    form_values[field] = values[field]
                except Exception:
                    form_values[field] = False
            partner.sudo().write(form_values)
            return request.redirect("/my/home")
        values.update(
            {
                "partner": partner,
                "page_name": "my_details",
            }
        )
        response = request.render("portal.portal_my_details", values)
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @route(["/my/account/minecraft_remove"], type="http", auth="user", website=True)
    def my_account_minecraft_remove(self, **values):
        request.env.user.partner_id.gc_user_id = False
        return request.redirect("/my/account")

    @route(["/my/account/minecraft_auth"], type="http", auth="user", website=True)
    def my_account_minecraft_auth(self, **values):
        url = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/my/account/minecraft_auth"  # noqa: B950
        data = {
            "client_id": request.env["ir.config_parameter"]
            .sudo()
            .get_param("gigaclub.azure_client_id"),
            "client_secret": request.env["ir.config_parameter"]
            .sudo()
            .get_param("gigaclub.azure_client_secret"),
            "code": values.get("code", ""),
            "grant_type": "authorization_code",
            "redirect_uri": url,
        }
        response = requests.post("https://login.live.com/oauth20_token.srf", data=data)
        values = response.json()
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": f"d={values.get('access_token', '')}",
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response = requests.post(
            "https://user.auth.xboxlive.com/user/authenticate",
            data=json.dumps(data),
            headers=headers,
        )
        values = response.json()
        data = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    values.get("Token", ""),
                ],
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }
        response = requests.post(
            "https://xsts.auth.xboxlive.com/xsts/authorize",
            data=json.dumps(data),
            headers=headers,
        )
        values = response.json()
        data = {
            "identityToken": f"XBL3.0 x={values.get('DisplayClaims').get('xui')[0].get('uhs', '')}; {values.get('Token')}",  # noqa: B950
            "ensureLegacyEnabled": True,
        }
        response = requests.post(
            "https://api.minecraftservices.com/authentication/login_with_xbox",
            data=json.dumps(data),
            headers=headers,
        )
        values = response.json()
        headers["Authorization"] = f"Bearer {values.get('access_token', '')}"
        response = requests.get(
            "https://api.minecraftservices.com/minecraft/profile", headers=headers
        )
        values = response.json()
        mc_uuid = uuid.UUID(values.get("id", ""))
        mc_username = values.get("name", "")
        GCUser = request.env["gc.user"]
        gc_user = GCUser.search([("mc_uuid", "=", mc_uuid)], limit=1)
        if gc_user:
            request.env.user.partner_id.gc_user_id = gc_user
        else:
            request.env.user.partner_id.gc_user_id = GCUser.create(
                {
                    "mc_uuid": mc_uuid,
                    "name": mc_username,
                }
            )
        return request.redirect("/my/account")
