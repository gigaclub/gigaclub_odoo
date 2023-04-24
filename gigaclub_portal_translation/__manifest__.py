{
    "name": "GigaClub Portal Translation",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["gigaclub_portal", "gigaclub_translation"],
    "data": ["views/portal_templates.xml"],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "/gigaclub_portal_translation/static/libs/webui-adventure.js",
            "/gigaclub_portal_translation/static/css/style.css",
        ]
    },
    "installable": True,
    "auto_install": False,
}
