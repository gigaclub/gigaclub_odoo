{
    "name": "GigaClub IP System",
    "version": "16.0.1.0.0",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["gigaclub_base"],
    "data": [
        "security/ir.model.access.csv",
        "views/gc_ip_timestamp_views.xml",
        "views/gc_ip_views.xml",
        "views/gc_user_views.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
