from odoo.http import request

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal


class GigaClubPortalBuilderSystem(GigaClubPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "world_count" in counters:
            user = request.env.user.partner_id.gc_user_id
            values["world_count"] = (
                user
                and request.env["gc.builder.world"].search_count(
                    [
                        "|",
                        "|",
                        ("owner_id", "=", user.id),
                        ("permission_connector_ids.user_id", "in", user.ids),
                        (
                            "permission_connector_ids.team_id",
                            "in",
                            (
                                user.permission_connector_ids.mapped("team_id")
                                | request.env["gc.team"].search(
                                    [("owner_id", "=", user.id)]
                                )
                            ).ids,
                        ),
                    ]
                )
                or 0
            )
        return values
