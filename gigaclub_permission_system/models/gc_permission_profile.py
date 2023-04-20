from odoo import api, fields, models


class GCPermissionProfile(models.Model):
    _name = "gc.permission.profile"
    _inherits = {"gc.permission.profile.template": "permission_profile_template_id"}
    _description = "GigaClub Permission Profile"

    permission_profile_entry_ids = fields.One2many(
        comodel_name="gc.permission.profile.entry", inverse_name="permission_profile_id"
    )
    permission_profile_template_id = fields.Many2one(
        comodel_name="gc.permission.profile.template", required=True, ondelete="cascade"
    )
    permission_group_id = fields.Many2one(
        comodel_name="gc.permission.group", index=True, ondelete="cascade"
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            rec.permission_profile_entry_ids = [
                (0, 0, {"permission_profile_entry_template_id": template.id})
                for template in rec.permission_profile_template_id.permission_profile_entry_template_ids  # noqa: B950
            ]
        return res

    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (
                    rec.id,
                    ", ".join(
                        rec.permission_profile_entry_ids.mapped(
                            "permission_model_entry_id.name"
                        )
                    ),
                )
            )
        return result
