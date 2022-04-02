from odoo import fields, models


class GCPermissionGroup(models.Model):
    _name = "gc.permission.group"
    _description = "GigaClub Permission Group"

    name = fields.Char()
    description = fields.Text()
    permission_profile_ids = fields.Many2many(comodel_name="gc.permission.profile")
