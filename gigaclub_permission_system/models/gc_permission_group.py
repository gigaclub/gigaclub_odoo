from odoo import fields, models


class GCPermissionGroup(models.Model):
    _name = "gc.permission.group"
    _description = "GigaClub Permission Group"

    name = fields.Char()
    description = fields.Text()
    permission_profile_line_ids = fields.One2many(
        comodel_name="gc.permission.profile.line", inverse_name="permission_group_id"
    )
