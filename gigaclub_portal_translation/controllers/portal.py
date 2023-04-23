from odoo.http import request

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal


class GigaClubTranslationPortal(GigaClubPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "translation_count" in counters:
            user = request.env.user.partner_id.gc_user_id
            values["translation_count"] = (
                user and request.env["gc.translation"].search_count([]) or 0
            )
        return values
