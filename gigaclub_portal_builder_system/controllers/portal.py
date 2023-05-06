from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.fields import first
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class GigaClubPortalBuilderSystem(GigaClubPortal):
    _MANDATORY_WORLD_FIELDS = ["name", "world_type_id", "task_id"]

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

    @route("/my/world/<int:world_id>/delete", type="http", auth="user", website=True)
    def portal_my_world_delete(self, world_id, **kw):
        try:
            world_sudo = self._document_check_access("gc.builder.world", world_id)
        except (AccessError, MissingError):
            return request.redirect("/my")
        world_sudo.unlink()
        return request.redirect("/my/worlds")

    @route(
        "/my/world/<int:world_id>/permission_connector/<int:permission_connector_id>/delete/<string:delete_type>",  # noqa: B950
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_world_permission_connector_delete(
        self, world_id, permission_connector_id, delete_type, **kw
    ):
        try:
            world_sudo = self._document_check_access("gc.builder.world", world_id)
        except (AccessError, MissingError):
            return request.redirect("/my")
        if delete_type == "team":
            world_sudo.permission_connector_ids.filtered(
                lambda x: x.team_id.id == permission_connector_id
            ).unlink()
        else:
            world_sudo.permission_connector_ids.filtered(
                lambda x: x.user_id.id == permission_connector_id
            ).unlink()
        return request.redirect(f"/my/world/{world_id}/edit")

    @route("/my/world/create", type="http", auth="user", website=True)
    def portal_my_world_create(self, **kw):
        values = self._world_get_page_create_values(**kw)
        values.update({"error": {}, "error_message": [], "mode": "create"})
        if kw and request.httprequest.method == "POST":
            form = request.httprequest.form
            form_values = {
                "name": form.get("name", ""),
                "world_type_id": form.get("world_type_id", ""),
                "task_id": form.get("task_id", ""),
            }
            error, error_message = self.world_form_validate(form_values)
            values.update({"error": error, "error_message": error_message})
            values["world"].update(
                {
                    "name": form_values.get("name", False),
                    "world_type_id": form_values.get("world_type_id", False),
                    "task_id": form_values.get("task_id", False),
                }
            )
            if not error and not error_message:
                owner_id = request.env.user.partner_id.gc_user_id.id
                create_vals = {
                    "name": form_values.get("name", False),
                    "world_type_id": form_values.get("world_type_id", False),
                    "task_id": form_values.get("task_id", False),
                    "owner_id": owner_id,
                }
                values.update({"world": create_vals})
                world = request.env["gc.builder.world"].create(create_vals)
                return request.redirect("/my/world/{}/view".format(world.id))
        return request.render(
            "gigaclub_portal_builder_system.portal_my_world_form", values
        )

    @route(
        "/my/world/<int:world_id>/view",
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_world_view(self, world_id, **kw):
        try:
            world_sudo = self._document_check_access("gc.builder.world", world_id)
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._world_get_page_view_values(world_sudo, **kw)
        return request.render(
            "gigaclub_portal_builder_system.portal_my_world_view", values
        )

    @route("/my/world/<int:world_id>/edit", type="http", auth="user", website=True)
    def portal_my_world_edit(self, world_id, **kw):  # noqa: C901
        # TODO: take care of this complexity...
        try:
            world_sudo = self._document_check_access("gc.builder.world", world_id)
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._world_get_page_edit_values(world_sudo, **kw)
        values.update({"error": {}, "error_message": [], "mode": "edit"})
        if kw and request.httprequest.method == "POST":
            form = request.httprequest.form
            if form.get("user", False):
                return_redirect = request.redirect(
                    "/my/world/{}/edit".format(world_sudo.id)
                )
                form_values = {
                    "user": form.get("user", ""),
                    "invite_user": form.get("inviteuser", False),
                    "invite_team": form.get("inviteteam", False),
                    "remove_user": form.get("removeuser", False),
                    "remove_team": form.get("removeteam", False),
                    "save_world": form.get("saveworld", False),
                    "edit_world_type": form.get("editworldtype", False),
                }
                if not form_values.get("user", "").isnumeric():
                    return return_redirect
                user = world_sudo.env["gc.user"].browse(
                    int(form_values.get("user", ""))
                )
                if not user:
                    return return_redirect
                self._world_set_permissions(
                    world_sudo,
                    form_values.get("invite_user", False),
                    form_values.get("invite_team", False),
                    form_values.get("remove_user", False),
                    form_values.get("remove_team", False),
                    form_values.get("save_world", False),
                    form_values.get("edit_world_type", False),
                    user=user,
                )
                return return_redirect
            elif form.get("invite-user", False):
                return_redirect = request.redirect(
                    "/my/world/{}/edit".format(world_sudo.id)
                )
                invited_user_id = form.get("invite-user", False)
                if not invited_user_id.isnumeric():
                    return return_redirect
                user = world_sudo.env["gc.user"].browse(int(invited_user_id))
                if not user:
                    return return_redirect
                world_sudo.env["gc.request"].create(
                    {
                        "sender_id": f"{world_sudo._name},{world_sudo.id}",
                        "receiver_id": f"{user._name},{user.id}",
                        "request_type": "member_or_team_to_world_invitation",
                        "state": "waiting",
                    }
                )
                return return_redirect
            elif form.get("invite-team", False):
                return_redirect = request.redirect(
                    "/my/world/{}/edit".format(world_sudo.id)
                )
                invited_team_id = form.get("invite-team", False)
                if not invited_team_id.isnumeric():
                    return return_redirect
                team = world_sudo.env["gc.team"].browse(int(invited_team_id))
                if not team:
                    return return_redirect
                world_sudo.env["gc.request"].create(
                    {
                        "sender_id": f"{world_sudo._name},{world_sudo.id}",
                        "receiver_id": f"{team._name},{team.id}",
                        "request_type": "member_or_team_to_world_invitation",
                        "state": "waiting",
                    }
                )
                return return_redirect
            elif form.get("team", False):
                return_redirect = request.redirect(
                    "/my/world/{}/edit".format(world_sudo.id)
                )
                form_values = {
                    "team": form.get("team", ""),
                    "invite_user": form.get("inviteuser", False),
                    "invite_team": form.get("inviteteam", False),
                    "remove_user": form.get("removeuser", False),
                    "remove_team": form.get("removeteam", False),
                    "save_world": form.get("saveworld", False),
                    "edit_world_type": form.get("editworldtype", False),
                }
                if not form_values.get("team", "").isnumeric():
                    return return_redirect
                team = world_sudo.env["gc.user"].browse(
                    int(form_values.get("team", ""))
                )
                if not team:
                    return return_redirect
                self._world_set_permissions(
                    world_sudo,
                    form_values.get("invite_user", False),
                    form_values.get("invite_team", False),
                    form_values.get("remove_user", False),
                    form_values.get("remove_team", False),
                    form_values.get("save_world", False),
                    form_values.get("edit_world_type", False),
                    team=team,
                )
                return return_redirect
            elif form.get("name", False):
                form_values = {
                    "name": form.get("name", ""),
                    "world_type_id": int(form.get("world_type_id", "")),
                    "task_id": int(form.get("task_id", "")),
                }
                if form_values.get("name", "") == world_sudo.name:
                    del form_values["name"]
                error, error_message = self.world_form_validate(form_values, world_sudo)
                values.update({"error": error, "error_message": error_message})
                values["world"].update(
                    {
                        "name": form_values.get("name", world_sudo.name),
                        "world_type_id": form_values.get(
                            "world_type_id", world_sudo.world_type_id.id
                        ),
                        "task_id": form_values.get("task_id", world_sudo.task_id.id),
                    }
                )
                if not error and not error_message:
                    owner_id = request.env.user.partner_id.gc_user_id.id
                    write_vals = {
                        "name": form_values.get("name", world_sudo.name),
                        "world_type_id": form_values.get(
                            "world_type_id", world_sudo.world_type_id.id
                        ),
                        "task_id": form_values.get("task_id", world_sudo.task_id.id),
                        "owner_id": owner_id,
                    }
                    values.update({"team": write_vals})
                    world_sudo.write(write_vals)
                    return request.redirect("/my/world/{}/view".format(world_sudo.id))
        return request.render(
            "gigaclub_portal_builder_system.portal_my_world_form", values
        )

    def world_form_validate(self, values, world=False):
        error = dict()
        error_message = []
        if not world:
            for field_name in self._MANDATORY_WORLD_FIELDS:
                if not values.get(field_name):
                    error[field_name] = "missing"

        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        return error, error_message

    def _world_get_page_create_values(self, **kwargs):
        values = {
            "page_name": "world",
            "world": {
                "owner": request.env.user.partner_id.gc_user_id.display_name,
                "users": [],
                "teams": [],
                "worldtypes": request.env["gc.builder.world.type"]
                .search([])
                .mapped(
                    lambda x: {
                        "name": x.name,
                        "id": x.id,
                    }
                ),
                "tasks": request.env["project.task"]
                .search([])
                .mapped(
                    lambda x: {
                        "name": x.name,
                        "id": x.id,
                    }
                ),
            },
        }
        return self._get_page_view_values(
            request.env["gc.builder.world"],
            None,
            values,
            "my_worlds_history",
            False,
            **kwargs,
        )

    def _world_get_page_view_values(self, world, access_token=None, **kwargs):
        values = {
            "page_name": "world",
            "world": world,
        }
        return self._get_page_view_values(
            world, access_token, values, "my_worlds_history", False, **kwargs
        )

    def _world_get_page_edit_values(self, world, **kwargs):
        world_users = world.permission_connector_ids.mapped("user_id")
        world_teams = world.permission_connector_ids.mapped("team_id")
        values = {
            "page_name": "world",
            "world": {
                "id": world.id,
                "owner": world.owner_id.display_name,
                "name": world.name,
                "world_type_id": world.world_type_id.id,
                "task_id": world.task_id.id,
                "users": [
                    {
                        "id": user.id,
                        "name": user.display_name,
                        "permission_count": len(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            ).mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                        ),
                        "invite_user": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_user"  # noqa: B950
                                )
                            )
                        ),
                        "invite_team": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_team"  # noqa: B950
                                )
                            )
                        ),
                        "remove_user": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_user"  # noqa: B950
                                )
                            )
                        ),
                        "remove_team": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_team"  # noqa: B950
                                )
                            )
                        ),
                        "save_world": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_save_world"  # noqa: B950
                                )
                            )
                        ),
                        "edit_world_type": bool(
                            user.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_edit_world_type"  # noqa: B950
                                )
                            )
                        ),
                    }
                    for user in world_users
                ],
                "teams": [
                    {
                        "id": team.id,
                        "name": team.name,
                        "permission_count": len(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            ).mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                        ),
                        "invite_user": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_user"  # noqa: B950
                                )
                            )
                        ),
                        "invite_team": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_team"  # noqa: B950
                                )
                            )
                        ),
                        "remove_user": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_user"  # noqa: B950
                                )
                            )
                        ),
                        "remove_team": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_team"  # noqa: B950
                                )
                            )
                        ),
                        "save_world": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_save_world"  # noqa: B950
                                )
                            )
                        ),
                        "edit_world_type": bool(
                            team.permission_connector_ids.filtered(
                                lambda x: x.world_id == world
                            )
                            .mapped(
                                "permission_profile_ids."
                                "permission_profile_entry_ids.permission_model_entry_id"
                            )
                            .filtered(
                                lambda x: x
                                == request.env.ref(
                                    "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_edit_world_type"  # noqa: B950
                                )
                            )
                        ),
                    }
                    for team in world_teams
                ],
                "worldtypes": request.env["gc.builder.world.type"]
                .search([])
                .mapped(
                    lambda x: {
                        "name": x.name,
                        "id": x.id,
                    }
                ),
                "tasks": request.env["project.task"]
                .search([])
                .mapped(
                    lambda x: {
                        "name": x.name,
                        "id": x.id,
                    }
                ),
            },
            "users": [
                {"id": user.id, "name": user.display_name}
                for user in request.env["gc.user"].search(
                    [
                        (
                            "id",
                            "not in",
                            (
                                world_users
                                | world.owner_id
                                | request.env["gc.user"].concat(
                                    *[
                                        x
                                        for x in request.env["gc.request"]
                                        .search(
                                            [
                                                (
                                                    "sender_id",
                                                    "=",
                                                    f"gc.builder.world,{world.id}",
                                                ),
                                                (
                                                    "request_type",
                                                    "=",
                                                    "member_or_team_to_world_invitation",
                                                ),
                                                ("state", "=", "waiting"),
                                            ]
                                        )
                                        .mapped("receiver_id")
                                        if x._name == "gc.user"
                                    ]
                                )
                            ).ids,
                        )
                    ]
                )
            ],
            "teams": [
                {"id": team.id, "name": team.name}
                for team in request.env["gc.team"].search(
                    [
                        (
                            "id",
                            "not in",
                            (
                                world_teams
                                | request.env["gc.team"].concat(
                                    *[
                                        x
                                        for x in request.env["gc.request"]
                                        .search(
                                            [
                                                (
                                                    "sender_id",
                                                    "=",
                                                    f"gc.builder.world,{world.id}",
                                                ),
                                                (
                                                    "request_type",
                                                    "=",
                                                    "member_or_team_to_world_invitation",
                                                ),
                                                ("state", "=", "waiting"),
                                            ]
                                        )
                                        .mapped("receiver_id")
                                        if x._name == "gc.team"
                                    ]
                                )
                            ).ids,
                        )
                    ]
                )
            ],
        }
        return self._get_page_view_values(
            request.env["gc.team"], None, values, "my_teams_history", False, **kwargs
        )

    def _world_set_permissions(
        self,
        world,
        invite_user,
        invite_team,
        remove_user,
        remove_team,
        save_world,
        edit_world_type,
        team=False,
        user=False,
    ):
        existing_permission_connector = first(
            world.permission_connector_ids.filtered(
                lambda x: x.user_id == user or x.team_id == team
            )
        )
        if not existing_permission_connector:
            existing_permission_connector = request.env[
                "gc.permission.connector"
            ].create(
                {
                    "team_id": team and team.id,
                    "user_id": user and user.id,
                    "world_id": world.id,
                }
            )
        existing_permissions = existing_permission_connector.permission_group_ids.mapped(
            "permission_profile_ids.permission_profile_entry_template_ids.permission_model_entry_id"  # noqa: B950
        )
        new_permission_profile = self._get_permission_profile(
            invite_user,
            invite_team,
            remove_user,
            remove_team,
            save_world,
            edit_world_type,
            existing_permissions,
        )
        existing_permission_connector.permission_profile_ids = [
            (6, 0, new_permission_profile.ids)
        ]

    def _get_permission_profile(
        self,
        invite_user,
        invite_team,
        remove_user,
        remove_team,
        save_world,
        edit_world_type,
        existing_permissions,
    ):
        permissions = request.env["gc.permission.model.entry"]
        invite_user_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_user"
        )
        if invite_user and invite_user_permission not in existing_permissions:
            permissions |= invite_user_permission
        invite_team_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_invite_team"
        )
        if invite_team and invite_team_permission not in existing_permissions:
            permissions |= invite_team_permission
        remove_user_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_user"
        )
        if remove_user and remove_user_permission not in existing_permissions:
            permissions |= remove_user_permission
        remove_team_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_remove_team"
        )
        if remove_team and remove_team_permission not in existing_permissions:
            permissions |= remove_team_permission
        save_world_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_save_world"
        )
        if save_world and save_world_permission not in existing_permissions:
            permissions |= save_world_permission
        edit_world_type_permission = request.env.ref(
            "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_edit_world_type"  # noqa: B950
        )
        if edit_world_type and edit_world_type_permission not in existing_permissions:
            permissions |= edit_world_type_permission
        new_permission_profile = request.env["gc.permission.profile"].create(
            {
                "permission_profile_entry_ids": [
                    (0, 0, {"permission_model_entry_id": permission.id})
                    for permission in permissions
                ]
            }
        )
        return new_permission_profile
