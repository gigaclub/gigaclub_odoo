{
    "name": "GigaClub Ban System",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["gigaclub_ip_system"],
    "data": [
        "security/ir.model.access.csv",
        "views/gc_user_views.xml",
        "views/menu_views.xml",
        "views/gc_warning_type_views.xml",
        "views/gc_warning_views.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
