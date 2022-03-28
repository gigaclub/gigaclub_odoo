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
