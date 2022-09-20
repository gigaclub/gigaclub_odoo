from odoo import fields, models


class GCPermissionProfileEntryTemplate(models.Model):
    _name = "gc.permission.profile.entry.template"
    _description = "GigaClub Permission Profile Entry Template"

    permission_model_entry_id = fields.Many2one(
        comodel_name="gc.permission.model.entry"
    )
    permission_profile_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.template", index=True
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.permission_model_entry_id.name))
        return result
