from odoo import fields, models


class GCPermissionProfile(models.Model):
    _name = "gc.permission.profile"
    _description = "GigaClub Permission Profile"

    read = fields.Boolean()
    write = fields.Boolean()
    create = fields.Boolean()
    delete = fields.Boolean()
