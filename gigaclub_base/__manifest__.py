{
    "name": "GigaClub Base",
    "version": "16.0.1.0.0",
    "summary": "GigaClub Base Module",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["base_setup"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/menu_views.xml",
        "views/gc_user_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
