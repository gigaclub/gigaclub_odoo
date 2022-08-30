from odoo import _
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class GigaClubPortalTeam(GigaClubPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "team_count" in counters:
            user = request.env.user.partner_id.gc_user_id
            values["team_count"] = (
                user
                and request.env["gc.team"].search_count(
                    [
                        "|",
                        ("owner_id", "=", user.id),
                        ("permission_connector_ids.user_id", "in", user.ids),
                    ]
                )
                or 0
            )
        return values

    @route(
        ["/my/teams", "/my/teams/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_projects(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        Teams = request.env["gc.team"]
        user = request.env.user.partner_id.gc_user_id
        domain = [
            "|",
            ("owner_id", "=", user.id),
            ("permission_connector_ids.user_id", "in", user.ids),
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

        team_count = Teams.search_count(domain)

        pager = portal_pager(
            url="/my/teams",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=team_count,
            page=page,
            step=self._items_per_page,
        )
        teams = Teams.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "teams": teams,
                "page_name": "team",
                "default_url": "/my/teams",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("gigaclub_portal_team.portal_my_teams", values)

    @route(
        "/my/team/<int:team_id>/<any('view', 'edit', 'create', 'delete'):mode>",
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_team(self, team_id, mode):
        self._prepare_portal_layout_values()
        request.env["gc.team"]
        request.env.user.partner_id.gc_user_id
