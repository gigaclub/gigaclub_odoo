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
            if values.get("auth-code"):
                gc_user = request.env["gc.user"].search(
                    [("auth_token", "=", values.get("auth-code"))], limit=1
                )
                if request.env.user.partner_id.gc_user_id and gc_user:
                    mc_uuid = request.env.user.partner_id.gc_user_id.with_context(
                        get_mc_uuid_back=True
                    ).merge_users(gc_user)
                    request.env.user.partner_id.gc_user_id.mc_uuid = mc_uuid
                elif gc_user:
                    request.env.user.partner_id.gc_user_id = gc_user
                return request.redirect("/my/account")
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
        request.env.user.partner_id.gc_user_id.mc_uuid = False
        return request.redirect("/my/account")

    @route(["/my/account/discord_remove"], type="http", auth="user", website=True)
    def my_account_discord_remove(self, **values):
        request.env.user.partner_id.gc_user_id.discord_uuid = False
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
        response = requests.post(
            "https://login.live.com/oauth20_token.srf", data=data, timeout=5
        )
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
            timeout=5,
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
            timeout=5,
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
            timeout=5,
        )
        values = response.json()
        headers["Authorization"] = f"Bearer {values.get('access_token', '')}"
        response = requests.get(
            "https://api.minecraftservices.com/minecraft/profile",
            headers=headers,
            timeout=5,
        )
        values = response.json()
        mc_uuid = uuid.UUID(values.get("id", ""))
        mc_username = values.get("name", "")
        GCUser = request.env["gc.user"]
        gc_user = GCUser.search([("mc_uuid", "=", mc_uuid)], limit=1)
        if request.env.user.partner_id.gc_user_id:
            if gc_user:
                request.env.user.partner_id.gc_user_id.merge_users(gc_user)
            request.env.user.partner_id.gc_user_id.mc_uuid = mc_uuid
        elif gc_user:
            request.env.user.partner_id.gc_user_id = gc_user
        else:
            request.env.user.partner_id.gc_user_id = GCUser.create(
                {
                    "mc_uuid": mc_uuid,
                    "name": mc_username,
                }
            )
        return request.redirect("/my/account")

    @route(["/my/account/discord_auth"], type="http", auth="user", website=True)
    def my_account_discord_auth(self, **values):
        url = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/my/account/discord_auth"  # noqa: B950
        data = {
            "client_id": request.env["ir.config_parameter"]
            .sudo()
            .get_param("gigaclub.discord_client_id"),
            "client_secret": request.env["ir.config_parameter"]
            .sudo()
            .get_param("gigaclub.discord_client_secret"),
            "grant_type": "authorization_code",
            "code": values.get("code"),
            "redirect_uri": url,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()
        values = response.json()
        access_token = values.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://discord.com/api/v10/users/@me", headers=headers, timeout=5
        )
        result = response.json()
        discord_uuid = result.get("id")
        discord_name = result.get("name")
        GCUser = request.env["gc.user"]
        gc_user = GCUser.search([("discord_uuid", "=", discord_uuid)], limit=1)
        if request.env.user.partner_id.gc_user_id:
            if gc_user:
                request.env.user.partner_id.gc_user_id.merge_users(gc_user)
            request.env.user.partner_id.gc_user_id.discord_uuid = discord_uuid
        elif gc_user:
            request.env.user.partner_id.gc_user_id = gc_user
        else:
            request.env.user.partner_id.gc_user_id = GCUser.create(
                {
                    "name": discord_name,
                    "discord_uuid": discord_uuid,
                }
            )
        return request.redirect("/my/account")
