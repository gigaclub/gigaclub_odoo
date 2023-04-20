from odoo import api, fields, models


class GCPermissionProfileEntry(models.Model):
    _name = "gc.permission.profile.entry"
    _inherits = {
        "gc.permission.profile.entry.template": "permission_profile_entry_template_id"
    }
    _description = "GigaClub Permission Profile Entry"

    permission_model_entry_id = fields.Many2one(
        comodel_name="gc.permission.model.entry", ondelete="cascade"
    )
    permission_profile_id = fields.Many2one(
        comodel_name="gc.permission.profile",
        required=True,
        index=True,
        ondelete="cascade",
    )
    permission_profile_entry_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.entry.template",
        required=True,
        ondelete="cascade",
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            rec.permission_model_entry_id |= (
                rec.permission_profile_entry_template_id.permission_model_entry_id
            )
        return res

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.permission_model_entry_id.name))
        return result
