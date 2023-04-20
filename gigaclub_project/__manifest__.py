{
    "name": "GigaClub Project",
    "version": "16.0.1.0.0",
    "summary": "GigaClub Project Extension",
    "category": "GigaClub",
    "author": "GigaClub",
    "website": "https://github.com/GigaClub/gigaclub_odoo",
    "license": "AGPL-3",
    "depends": ["gigaclub_team", "project_type"],
    "data": ["views/project_project_view.xml", "views/project_task_view.xml"],
    "installable": True,
    "auto_install": False,
    "pre_init_hook": "pre_init_hook",
}
