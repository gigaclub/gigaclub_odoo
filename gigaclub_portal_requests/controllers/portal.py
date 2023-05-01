from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class GigaClubPortalTeam(GigaClubPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "request_count" in counters:
            user = request.env.user.partner_id.gc_user_id
            values["request_count"] = (
                user
                and request.env["gc.request"].search_count(
                    [
                        ("state", "=", "waiting"),
                        "|",
                        ("receiver_id", "=", f"gc.user,{user.id}"),
                        (
                            "receiver_id",
                            "in",
                            [
                                f"gc.team,{team.id}"
                                for team in (
                                    user.permission_connector_ids.mapped("team_id")
                                    | request.env["gc.team"].search(
                                        [("owner_id", "=", user.id)]
                                    )
                                )
                            ],
                        ),
                    ]
                )
                or 0
            )
        return values

    @route(
        ["/my/requests", "/my/requests/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_teams(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        Requests = request.env["gc.request"]
        user = request.env.user.partner_id.gc_user_id
        domain = [
            ("state", "=", "waiting"),
            "|",
            ("receiver_id", "=", f"gc.user,{user.id}"),
            (
                "receiver_id",
                "in",
                [
                    f"gc.team,{team.id}"
                    for team in (
                        user.permission_connector_ids.mapped("team_id")
                        | request.env["gc.team"].search([("owner_id", "=", user.id)])
                    )
                ],
            ),
        ]

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
        }
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        request_count = Requests.search_count(domain)

        pager = portal_pager(
            url="/my/requests",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=request_count,
            page=page,
            step=self._items_per_page,
        )
        requests = Requests.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_requests_history"] = requests.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "gcrequests": requests,
                "page_name": "request",
                "default_url": "/my/requests",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("gigaclub_portal_requests.portal_my_requests", values)

    @route(
        ["/my/request/<int:request_id>/accept"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_request_accept(self, request_id, **kwargs):
        try:
            request_sudo = self._document_check_access("gc.request", request_id)
        except (AccessError, MissingError):
            return request.redirect("/my")
        redirect = request.redirect("/my/requests")
        if request_sudo.state != "waiting":
            return redirect
        if request_sudo.request_type == "member_to_team_invitation":
            team = request_sudo.sender_id
            user = request_sudo.receiver_id
            team.permission_connector_ids |= request_sudo.env[
                "gc.permission.connector"
            ].create(
                {
                    "user_id": user.id,
                }
            )
        elif request_sudo.request_type == "member_or_team_to_world_invitation":
            team_or_user = request_sudo.sender_id
            world = request_sudo.receiver_id
            if team_or_user._name == "gc.user":
                world.permission_connector_ids |= request_sudo.env[
                    "gc.permission.connector"
                ].create(
                    {
                        "user_id": team_or_user.id,
                        "permission_profile_ids": [
                            (
                                0,
                                0,
                                {
                                    "permission_profile_template_id": self.env.ref(
                                        "gigaclub_builder_system.gc_permission_profile_template_builder_system_default"  # noqa: B950
                                    ).id,
                                },
                            )
                        ],
                    }
                )
            elif team_or_user._name == "gc.team":
                permission_connectors = [
                    (
                        0,
                        0,
                        {
                            "team_id": team_or_user.id,
                            "permission_profile_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "permission_profile_template_id": self.env.ref(
                                            "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ]
                for user in team_or_user.permission_connector_ids.mapped("user_id"):
                    permission_connectors.append(
                        (
                            0,
                            0,
                            {
                                "user_id": user.id,
                                "bound_to_team": True,
                                "permission_profile_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "permission_profile_template_id": self.env.ref(
                                                "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    )
        request_sudo.state = "accepted"
        return redirect

    @route(
        ["/my/request/<int:request_id>/deny"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_request_deny(self, request_id, **kwargs):
        try:
            request_sudo = self._document_check_access("gc.request", request_id)
        except (AccessError, MissingError):
            return request.redirect("/my")
        request_sudo.state = "denied"
        return request.redirect("/my/requests")
