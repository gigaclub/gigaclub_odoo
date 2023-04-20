from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.fields import first
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class GigaClubPortalTeam(GigaClubPortal):
    _MANDATORY_TEAM_FIELDS = ["name"]

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
    def portal_my_teams(
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

    @route("/my/team/<int:team_id>/edit", type="http", auth="user", website=True)
    def portal_my_team_edit(self, team_id, **kw):
        try:
            team_sudo = self._document_check_access("gc.team", team_id)
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._team_get_page_edit_values(team_sudo, **kw)
        values.update({"error": {}, "error_message": [], "mode": "edit"})
        if kw and request.httprequest.method == "POST":
            form = request.httprequest.form
            if form.get("user", False):
                return_redirect = request.redirect(
                    "/my/team/{}/edit".format(team_sudo.id)
                )
                form_values = {
                    "user": form.get("user", ""),
                    "groups": form.getlist("groups"),
                    "edit_team": form.get("editteam", False),
                    "invite_user": form.get("inviteuser", False),
                    "kick_user": form.get("kickuser", False),
                    "create_world_as_team": form.get("createworldasteam", False),
                }
                if not form_values.get("user", "").isnumeric():
                    return return_redirect
                user = team_sudo.env["gc.user"].browse(int(form_values.get("user", "")))
                if not user:
                    return return_redirect
                self._team_user_set_groups(team_sudo, user, form.getlist("groups"))
                self._team_user_set_permissions(
                    team_sudo,
                    user,
                    form_values.get("edit_team", False),
                    form_values.get("invite_user", False),
                    form_values.get("kick_user", False),
                    form_values.get("create_world_as_team", False),
                )
                return return_redirect
            elif form.get("group-name", False):
                return_redirect = request.redirect(
                    "/my/team/{}/edit".format(team_sudo.id)
                )
                form_values = {
                    "name": form.get("group-name", False),
                    "description": form.get("group-description", False),
                    "edit_team": form.get("editteam", False),
                    "invite_user": form.get("inviteuser", False),
                    "kick_user": form.get("kickuser", False),
                    "create_world_as_team": form.get("createworldasteam", False),
                    "parent_group": form.get("parentgroup", False),
                    "child_groups": form.getlist("childgroups"),
                }
                new_permission_group = team_sudo.env["gc.permission.group"].create(
                    {
                        "name": form_values.get("name"),
                        "description": form_values.get("description"),
                        "parent_group_id": int(form_values.get("parent_group")),
                        "child_group_ids": [
                            (6, 0, [int(x) for x in form_values.get("child_groups")])
                        ],
                    }
                )
                existing_permissions = new_permission_group.permission_profile_ids.mapped(
                    "permission_profile_entry_template_ids.permission_model_entry_id"  # noqa: B950
                )
                new_permission_profile = self._team_get_permission_profile(
                    form_values.get("edit_team"),
                    form_values.get("invite_user"),
                    form_values.get("kick_user"),
                    form_values.get("create_world_as_team"),
                    existing_permissions,
                )
                new_permission_group.permission_profile_ids = [
                    (6, 0, new_permission_profile.ids)
                ]
                team_sudo.possible_permission_group_ids |= new_permission_group
                return return_redirect
            elif form.get("name", False):
                form_values = {
                    "name": form.get("name", ""),
                    "description": form.get("description", ""),
                }
                if form_values.get("name", "") == team_sudo.name:
                    del form_values["name"]
                error, error_message = self.team_form_validate(form_values, team_sudo)
                values.update({"error": error, "error_message": error_message})
                values["team"].update(
                    {
                        "name": form_values.get("name", team_sudo.name),
                        "description": form_values.get(
                            "description", team_sudo.description
                        ),
                    }
                )
                if not error and not error_message:
                    owner_id = request.env.user.partner_id.gc_user_id.id
                    write_vals = {
                        "name": form_values.get("name", team_sudo.name),
                        "description": form_values.get(
                            "description", team_sudo.description
                        ),
                        "owner_id": owner_id,
                    }
                    values.update({"team": write_vals})
                    team_sudo.write(write_vals)
                    return request.redirect("/my/team/{}/view".format(team_sudo.id))
        return request.render("gigaclub_portal_team.portal_my_team_form", values)

    @route("/my/team/create", type="http", auth="user", website=True)
    def portal_my_team_create(self, **kw):
        values = self._team_get_page_create_values(**kw)
        values.update({"error": {}, "error_message": [], "mode": "create"})
        if kw and request.httprequest.method == "POST":
            form = request.httprequest.form
            form_values = {
                "name": form.get("name", ""),
                "description": form.get("description", ""),
            }
            error, error_message = self.team_form_validate(form_values)
            values.update({"error": error, "error_message": error_message})
            values["team"].update(
                {
                    "name": form_values.get("name", False),
                    "description": form_values.get("description", False),
                }
            )
            if not error and not error_message:
                owner_id = request.env.user.partner_id.gc_user_id.id
                create_vals = {
                    "name": form_values.get("name", False),
                    "description": form_values.get("description", False),
                    "owner_id": owner_id,
                }
                values.update({"team": create_vals})
                team = request.env["gc.team"].create(create_vals)
                return request.redirect("/my/team/{}/view".format(team.id))
        return request.render("gigaclub_portal_team.portal_my_team_form", values)

    def team_form_validate(self, values, team=False):
        error = dict()
        error_message = []
        if not team:
            for field_name in self._MANDATORY_TEAM_FIELDS:
                if not values.get(field_name):
                    error[field_name] = "missing"

        if values.get("name"):
            if request.env["gc.team"].search([("name", "=ilike", values.get("name"))]):
                error["name"] = "already exists"
                error_message.append(_("Team name already exists!"))

        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        return error, error_message

    def _team_user_set_groups(self, team, user, groups):
        existing_permission_connector = first(
            team.permission_connector_ids.filtered(lambda x: x.user_id == user)
        )
        if not existing_permission_connector:
            existing_permission_connector = request.env[
                "gc.permission.connector"
            ].create({"team_id": team.id, "user_id": user.id})
        group_ids = [int(i) for i in list(filter(lambda x: x.isnumeric(), groups))]
        existing_permission_connector.permission_group_ids = [(6, 0, group_ids)]

    def _team_user_set_permissions(
        self, team, user, edit_team, invite_user, kick_user, create_world_as_team
    ):
        existing_permission_connector = first(
            team.permission_connector_ids.filtered(lambda x: x.user_id == user)
        )
        if not existing_permission_connector:
            existing_permission_connector = request.env[
                "gc.permission.connector"
            ].create({"team_id": team.id, "user_id": user.id})
        existing_permissions = existing_permission_connector.permission_group_ids.mapped(
            "permission_profile_ids.permission_profile_entry_template_ids.permission_model_entry_id"  # noqa: B950
        )
        new_permission_profile = self._team_get_permission_profile(
            edit_team,
            invite_user,
            kick_user,
            create_world_as_team,
            existing_permissions,
        )
        existing_permission_connector.permission_profile_ids = [
            (6, 0, new_permission_profile.ids)
        ]

    def _team_get_permission_profile(
        self,
        edit_team,
        invite_user,
        kick_user,
        create_world_as_team,
        existing_permissions,
    ):
        permissions = request.env["gc.permission.model.entry"]
        edit_team_permission = request.env.ref(
            "gigaclub_team.gc_permission_model_entry_gc_team_edit_team"
        )
        if edit_team and edit_team_permission not in existing_permissions:
            permissions |= edit_team_permission
        invite_user_permission = request.env.ref(
            "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"
        )
        if invite_user and invite_user_permission not in existing_permissions:
            permissions |= invite_user_permission
        kick_user_permission = request.env.ref(
            "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"
        )
        if kick_user and kick_user_permission not in existing_permissions:
            permissions |= kick_user_permission
        create_world_as_team_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_team_create_world_as_team"
        )
        if (
            create_world_as_team
            and create_world_as_team_permission not in existing_permissions
        ):
            permissions |= create_world_as_team_permission
        new_permission_profile = request.env["gc.permission.profile"].create(
            {
                "permission_profile_entry_ids": [
                    (0, 0, {"permission_model_entry_id": permission.id})
                    for permission in permissions
                ]
            }
        )
        return new_permission_profile

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

    def _team_get_page_edit_values(self, team, **kwargs):
        team_users = team.permission_connector_ids.mapped("user_id")
        values = {
            "page_name": "team",
            "team": {
                "owner": team.owner_id.display_name,
                "name": team.name,
                "description": team.description,
                "users": [
                    {
                        "id": user.id,
                        "name": user.display_name,
                        "group_count": len(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            ).mapped("permission_group_ids")
                        ),
                        "groups": [
                            {
                                "id": group.id,
                                "name": group.name,
                            }
                            for group in user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            ).mapped("permission_group_ids")
                        ],
                        "permission_count": len(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            ).mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                        ),
                        "edit_team": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_edit_team"
                                )
                            )
                        ),
                        "invite_user": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"  # noqa: B950
                                )
                            )
                        ),
                        "kick_user": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"  # noqa: B950
                                )
                            )
                        ),
                        "create_world_as_team": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.team_id == team
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_team_create_world_as_team"  # noqa: B950
                                )
                            )
                        ),
                    }
                    for user in team_users
                ],
                "groups": [
                    {
                        "id": group.id,
                        "name": group.name,
                        "description": group.description,
                        "permission_count": len(
                            group.permission_profile_ids.mapped(
                                "permission_profile_entry_ids"
                            )
                        ),
                        "edit_team": bool(
                            group.mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            ).filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_edit_team"
                                )
                            )
                        ),
                        "invite_user": bool(
                            group.mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            ).filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"  # noqa: B950
                                )
                            )
                        ),
                        "kick_user": bool(
                            group.mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            ).filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"  # noqa: B950
                                )
                            )
                        ),
                        "create_world_as_team": bool(
                            group.mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            ).filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_team_create_world_as_team"  # noqa: B950
                                )
                            )
                        ),
                        "parent_group": {
                            "id": group.parent_group_id.id,
                            "name": group.parent_group_id.name,
                        },
                        "child_groups": [
                            {"id": child_group.id, "name": child_group.name}
                            for child_group in group.child_group_ids
                        ],
                    }
                    for group in team.possible_permission_group_ids
                ],
            },
            "users": [
                {"id": user.id, "name": user.display_name}
                for user in request.env["gc.user"]
                .search([])
                .filtered(lambda x: x not in team_users and x != team.owner_id)
            ],
        }
        return self._get_page_view_values(
            request.env["gc.team"], None, values, "my_teams_history", False, **kwargs
        )
