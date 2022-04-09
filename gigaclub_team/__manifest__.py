{
    "name": "GigaClub Team",
    "version": "14.0.1.0.0",
    "summary": "GigaClub Team Module",
    "category": "GigaClub",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net/",
    "license": "AGPL-3",
    "depends": ["gigaclub_requests", "gigaclub_permission_system"],
    "data": [
        "data/gc_permission_model_data.xml",
        "views/gc_team_view.xml",
        "views/menu_views.xml",
        "views/gc_user_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
