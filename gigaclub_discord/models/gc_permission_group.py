from odoo import fields, models


class GigaClubPermissionGroup(models.Model):
    _inherit = "gc.permission.group"

    role_ids = fields.One2many(
        comodel_name="gc.discord.role", inverse_name="permission_group_id"
    )
