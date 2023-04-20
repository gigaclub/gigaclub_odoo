from odoo import fields, models


class GCPermissionProfileTemplate(models.Model):
    _name = "gc.permission.profile.template"
    _description = "GigaClub Permission Profile Template"

    permission_model_ids = fields.Many2many(comodel_name="gc.permission.model")
    permission_profile_entry_template_ids = fields.One2many(
        comodel_name="gc.permission.profile.entry.template",
        inverse_name="permission_profile_template_id",
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (
                    rec.id,
                    ", ".join(
                        rec.permission_profile_entry_template_ids.mapped(
                            "permission_model_entry_id.name"
                        )
                    ),
                )
            )
        return result
