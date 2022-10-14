{
    "name": "GigaClub Builder System",
    "version": "16.0.1.0.0",
    "summary": "GigaClub Builder System Module",
    "category": "GigaClub",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net",
    "license": "AGPL-3",
    "depends": ["gigaclub_translation", "gigaclub_project"],
    "data": [
        "data/gc_builder_world_type_data.xml",
        "data/gc_permission_model_data.xml",
        "data/gc_permission_model_entry_data.xml",
        "data/gc_permission_profile_template_data.xml",
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        "views/gc_builder_world_views.xml",
        "views/gc_builder_world_type_views.xml",
        "views/gc_permission_connector_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
