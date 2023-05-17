from odoo import api, fields, models


class GCIpTimestamp(models.Model):
    _name = "gc.ip.timestamp"
    _description = "GigaClub IP Timestamp"

    ip_id = fields.Many2one(comodel_name="gc.ip")
    user_id = fields.Many2one(comodel_name="gc.user", index=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.calculate_ip_cycle()
        return records

    def calculate_ip_cycle(self):
        # TODO check for different ip's between...
        self.ensure_one()
        res1 = self.read_group(
            domain=[("user_id", "=", self.user_id.id)],
            fields=["create_date:min"],
            groupby=["ip_id"],
        )
        res2 = self.read_group(
            domain=[("user_id", "=", self.user_id.id)],
            fields=["create_date:max"],
            groupby=["ip_id"],
        )
        res1.extend(res2)
        # Assuming `res` contains the result from the read_group queries
        ip_ids = {item["ip_id"][0] for item in res1}  # Extract unique ip_id values

        time_cycles = []

        for ip_id in ip_ids:
            create_dates = [
                item["create_date"] for item in res1 if item["ip_id"][0] == ip_id
            ]
            time_diff = max(create_dates) - min(create_dates)
            time_cycles.append(time_diff.total_seconds() / 60 / 60)
        avg_cycle = sum(time_cycles) / len(time_cycles)
        if avg_cycle > 24:
            self.user_id.ip_cycle = avg_cycle
