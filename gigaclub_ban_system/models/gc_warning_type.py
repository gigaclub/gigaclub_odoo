from odoo import fields, models


class GCWarningType(models.Model):
    _name = "gc.warning.type"
    _description = "GigaClub Warning Type"

    name = fields.Char()
    description = fields.Text()
    ban_time = fields.Float()
    expiration_time = fields.Float()
