from odoo import api, fields, models


class GCIpTimestamp(models.Model):
    _name = "gc.ip.timestamp"
    _description = "GigaClub IP Timestamp"

    ip_id = fields.Many2one(comodel_name="gc.ip")
    user_id = fields.Many2one(comodel_name="gc.user", index=True)

    @api.model
    def get_blocked_ips(self):
        return [{"ipv4_hash": rec} for rec in self.filtered(lambda x: x.ip_id.blocked)]
