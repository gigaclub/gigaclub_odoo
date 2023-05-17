from datetime import datetime, timedelta

from odoo import api, fields, models


class GCWarning(models.Model):
    _name = "gc.warning"
    _description = "GigaClub Warning"

    user_id = fields.Many2one(comodel_name="gc.user", index=True)
    warning_type_id = fields.Many2one(comodel_name="gc.warning.type")
    ban_time = fields.Float()
    expiration_datetime = fields.Datetime()
    points = fields.Integer(related="warning_type_id.points", readonly=True)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.ban_time = rec.warning_type_id.ban_time
            expiration_time = int(rec.warning_type_id.expiration_time * 60 * 60)
            rec.expiration_datetime = datetime.now() + timedelta(
                seconds=expiration_time
            )
            rec.with_delay(eta=expiration_time).set_warning_active_false()
        return records

    def set_warning_active_false(self):
        self.ensure_one()
        self.active = False
