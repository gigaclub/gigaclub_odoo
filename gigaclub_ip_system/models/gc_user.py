from odoo import api, fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    ip_timestamp_ids = fields.One2many(
        comodel_name="gc.ip.timestamp", inverse_name="user_id"
    )
    ip_cycle = fields.Float(default=24.0)

    @api.model
    def make_ip_entry(self, player_uuid, hashed_ipv4_address):
        user = self.search([("mc_uuid", "=", player_uuid)], limit=1)
        ip = self.env["gc.ip"].search(
            [("ipv4_hash", "=", hashed_ipv4_address)], limit=1
        )
        if not ip:
            ip = self.env["gc.ip"].create({"ipv4_hash": hashed_ipv4_address})
        user.write({"ip_timestamp_ids": [(0, 0, {"user_id": user.id, "ip_id": ip.id})]})
        return 0

    @api.model
    def get_last_ip_hash(self, player_uuid) -> str:
        user = self.search([("mc_uuid", "=", player_uuid)], limit=1)
        last_ip_hash = str(
            user.ip_timestamp_ids.sorted("create_date", reverse=True)[
                :1
            ].ip_id.ipv4_hash
        )
        return last_ip_hash
