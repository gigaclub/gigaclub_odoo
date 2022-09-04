from odoo import _
from odoo.exceptions import AccessError, MissingError
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
        request.session["my_teams_history"] = teams.ids[:100]

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
        "/my/team/<int:team_id>/view",
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_team_view(self, team_id, **kw):
        try:
            team_sudo = self._document_check_access("gc.team", team_id)
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._team_get_page_view_values(team_sudo, **kw)
        return request.render("gigaclub_portal_team.portal_my_team_view", values)

    @route("/my/team/create", type="http", auth="user", website=True)
    def portal_my_team_create(self, **kw):
        values = self._team_get_page_create_values(**kw)
        return request.render("gigaclub_portal_team.portal_my_team_form", values)

    @route("/my/team/create/save", type="http", auth="user", website=True)
    def portal_my_team_create_save(self, **kw):
        GCTeam = request.env["gc.team"]
        owner_id = request.env.user.partner_id.gc_user_id.id
        values = {
            "name": kw.get("name", ""),
            "description": kw.get("description", ""),
            "owner_id": owner_id,
        }
        team = GCTeam.create(values)
        return request.redirect("/my/team/{}/view".format(team.id))

    def _team_get_page_view_values(self, team, access_token=None, **kwargs):
        values = {
            "page_name": "team",
            "team": team,
        }
        return self._get_page_view_values(
            team, access_token, values, "my_teams_history", False, **kwargs
        )

    def _team_get_page_create_values(self, **kwargs):
        values = {
            "page_name": "team",
            "team": {
                "owner": request.env.user.partner_id.gc_user_id.display_name,
                "users": [],
                "permission_groups": [],
            },
        }
        return self._get_page_view_values(
            request.env["gc.team"], None, values, "my_teams_history", False, **kwargs
        )
