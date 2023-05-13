from datetime import datetime, timedelta

from odoo import api, fields, models


class GCWarning(models.Model):
    _name = "gc.warning"
    _description = "GigaClub Warning"

    user_id = fields.Many2one(comodel_name="gc.user", index=True)
    warning_type_id = fields.Many2one(comodel_name="gc.warning.type")
    ban_expiration_datetime = fields.Datetime(compute="_compute_ban_time", store=True)
    expiration_datetime = fields.Datetime(
        compute="_compute_expiration_time", store=True
    )
    points = fields.Integer(related="warning_type_id.points", readonly=True)

    @api.depends("warning_type_id.ban_time", "user_id.warning_ids")
    def _compute_ban_time(self):
        for rec in self:
            ban_time = (
                (rec.warning_type_id.ban_time ** len(rec.user_id.warning_ids)) * 60 * 60
            )
            expiration_datetime = datetime.now() + timedelta(seconds=ban_time)
            rec.ban_expiration_datetime = expiration_datetime

    @api.depends("warning_type_id.expiration_time", "user_id.warning_ids")
    def _compute_expiration_time(self):
        for rec in self:
            expiration_time = (
                (rec.warning_type_id.expiration_time ** len(rec.user_id.warning_ids))
                * 60
                * 60
            )
            expiration_datetime = datetime.now() + timedelta(seconds=expiration_time)
            rec.expiration_datetime = expiration_datetime
