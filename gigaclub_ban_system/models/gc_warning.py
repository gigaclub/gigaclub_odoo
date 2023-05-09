from odoo import fields, models


class GCWarning(models.Model):
    _name = "gc.warning"
    _description = "GigaClub Warning"

    user_id = fields.Many2one(comodel_name="gc.user")
    warning_type = fields.Many2one(comodel_name="gc.warning.type")
    expiration_datetime = fields.Datetime()
