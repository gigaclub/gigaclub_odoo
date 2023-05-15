from odoo import fields, models


class GCIpTimestamp(models.Model):
    _name = "gc.ip.timestamp"
    _description = "GigaClub IP Timestamp"

    ip_id = fields.Many2one(comodel_name="gc.ip")
    user_id = fields.Many2one(comodel_name="gc.user", index=True)
