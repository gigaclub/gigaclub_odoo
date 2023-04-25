from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route

from odoo.addons.gigaclub_portal.controllers.portal import GigaClubPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class GigaClubTranslationPortal(GigaClubPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "translation_count" in counters:
            user = request.env.user.partner_id.gc_user_id
            values["translation_count"] = (
                user and request.env["gc.translation"].search_count([]) or 0
            )
        return values

    @route(
        ["/my/translations", "/my/translations/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_translations(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        Translations = request.env["gc.translation"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
            "category": {"label": _("Category"), "order": "category"},
        }
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        translation_count = Translations.search_count(domain)

        pager = portal_pager(
            url="/my/translations",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=translation_count,
            page=page,
            step=self._items_per_page,
        )
        translations = Translations.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_translations_history"] = translations.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "translations": translations,
                "page_name": "translation",
                "default_url": "/my/translations",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render(
            "gigaclub_portal_translation.portal_my_translations", values
        )

    @route(
        "/my/translation/<int:translation_id>/view",
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_translation_view(self, translation_id, **kw):
        try:
            translation_sudo = self._document_check_access(
                "gc.translation", translation_id
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._translation_get_page_view_values(translation_sudo, **kw)
        return request.render(
            "gigaclub_portal_translation.portal_my_translation_view", values
        )

    def _translation_get_page_view_values(
        self, translation, access_token=None, **kwargs
    ):
        values = {
            "page_name": "translation",
            "translation": translation,
        }
        return self._get_page_view_values(
            translation,
            access_token,
            values,
            "my_translations_history",
            False,
            **kwargs
        )
