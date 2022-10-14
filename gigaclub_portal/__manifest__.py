{
    "name": "GigaClub Portal",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net",
    "license": "AGPL-3",
    "depends": ["gigaclub_project", "portal"],
    "data": [
        "views/portal_templates.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "/gigaclub_portal/static/libs/js/bootstrap-select.js",
            "/gigaclub_portal/static/libs/css/bootstrap-select.css",
        ]
    },
    "installable": True,
    "auto_install": False,
}
