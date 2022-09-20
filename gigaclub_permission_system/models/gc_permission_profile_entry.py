from odoo import fields, models, api


class GCPermissionProfileEntry(models.Model):
    _name = "gc.permission.profile.entry"
    _inherits = {
        "gc.permission.profile.entry.template": "permission_profile_entry_template_id"
    }
    _description = "GigaClub Permission Profile Entry"

    permission_model_entry_id = fields.Many2one(
        comodel_name="gc.permission.model.entry"
    )
    permission_profile_id = fields.Many2one(
        comodel_name="gc.permission.profile", required=True, index=True
    )
    permission_profile_entry_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.entry.template", required=True
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res.filtered(lambda x: not x.permission_model_entry_id):
            rec.permission_model_entry_id = rec.permission_profile_entry_template_id.permission_model_entry_id
        return res
