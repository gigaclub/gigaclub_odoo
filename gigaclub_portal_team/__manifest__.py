{
    "name": "GigaClub Portal Team",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net",
    "license": "AGPL-3",
    "depends": ["gigaclub_portal", "gigaclub_builder_system"],
    "data": ["views/portal_templates.xml"],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "/gigaclub_portal_team/static/src/js/gigaclub_portal_team.js",
            "/gigaclub_portal_team/static/src/scss/gigaclub_portal_team.scss",
        ]
    },
    "installable": True,
    "auto_install": False,
}
