{
    "name": "GigaClub Base",
    "version": "14.0.1.0.0",
    "summary": "GigaClub Base Module",
    "category": "GigaClub",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net/",
    "license": "GPL-3",
    "depends": ["base_setup"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/menu_views.xml",
        "views/gc_user_views.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
