from odoo import models


class GCUser(models.Model):
    _name = "gc.user"
    _inherit = ["gc.user", "gc.permission.mixin"]
