from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    ip_ids = fields.Many2many(comodel_name="gc.ip")
