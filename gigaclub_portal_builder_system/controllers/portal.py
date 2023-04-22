from odoo import _
from odoo.exceptions import AccessError, MissingError
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
            **kwargs
        )

    def _world_get_page_view_values(self, world, access_token=None, **kwargs):
        values = {
            "page_name": "world",
            "world": world,
        }
        return self._get_page_view_values(
            world, access_token, values, "my_worlds_history", False, **kwargs
        )
