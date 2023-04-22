{
    "name": "GigaClub Portal Builder System",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["gigaclub_portal_team"],
    "data": ["views/portal_templates.xml"],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "/gigaclub_portal_builder_system/static/src/js/gigaclub_portal_builder_system.esm.js",  # noqa: B950
        ]
    },
    "installable": True,
    "auto_install": False,
}
