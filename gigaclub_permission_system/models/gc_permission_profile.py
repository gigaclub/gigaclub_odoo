from odoo import fields, models, api


class GCPermissionProfile(models.Model):
    _name = "gc.permission.profile"
    _inherits = {"gc.permission.profile.template": "permission_profile_template_id"}
    _description = "GigaClub Permission Profile"

    permission_profile_entry_ids = fields.One2many(
        comodel_name="gc.permission.profile.entry", inverse_name="permission_profile_id"
    )
    permission_profile_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.template", required=True
    )
    permission_group_id = fields.Many2one(
        comodel_name="gc.permission.group", index=True
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res.filtered(lambda x: not x.permission_profile_entry_ids):
            rec.permission_profile_entry_ids = [(
                0, 0, {
                    "permission_profile_entry_template_id": template.id
                }
            ) for template in rec.permission_profile_template_id.permission_profile_entry_template_ids]
        return res
