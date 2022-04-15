from odoo import fields, models


class GCPermissionProfileEntryTemplate(models.Model):
    _name = "gc.permission.profile.entry.template"
    _description = "GigaClub Permission Profile Entry Template"

    permission_model_entry_id = fields.Many2one(
        comodel_name="gc.permission.model.entry", required=True
    )
    gc_permission_profile_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.template", required=True, index=True
    )
