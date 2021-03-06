{
    "name": "GigaClub Translation",
    "version": "14.0.1.0.0",
    "summary": "GigaClub Translation Module",
    "category": "Translation",
    "author": "GigaClub.net",
    "website": "https://GigaClub.net/",
    "license": "AGPL-3",
    "depends": ["gigaclub_base", "minecraft_field_tellraw"],
    "data": [
        "data/res_lang_data.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/gc_translation_views.xml",
        "views/gc_translation_entry_views.xml",
        "views/gc_user_views.xml",
        "views/menu_views.xml",
    ],
    "qweb": [
        "static/src/xml/minecraft_tellraw_field.xml",
    ],
    "installable": True,
    "auto_install": False,
}
