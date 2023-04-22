from odoo import _
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


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

    @route(
        ["/my/worlds", "/my/worlds/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_worlds(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        Worlds = request.env["gc.builder.world"]
        user = request.env.user.partner_id.gc_user_id
        domain = [
            "|",
            "|",
            ("owner_id", "=", user.id),
            ("permission_connector_ids.user_id", "in", user.ids),
            (
                "permission_connector_ids.team_id",
                "in",
                (
                    user.permission_connector_ids.mapped("team_id")
                    | request.env["gc.team"].search([("owner_id", "=", user.id)])
                ).ids,
            ),
        ]

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        world_count = Worlds.search_count(domain)

        pager = portal_pager(
            url="/my/worlds",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=world_count,
            page=page,
            step=self._items_per_page,
        )
        worlds = Worlds.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_worlds_history"] = worlds.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "worlds": worlds,
                "page_name": "world",
                "default_url": "/my/worlds",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("gigaclub_portal_builder_system.portal_my_worlds", values)
