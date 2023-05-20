from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    coins = fields.Integer()
