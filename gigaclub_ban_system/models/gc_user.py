from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.fields import first


class GCUser(models.Model):
    _inherit = "gc.user"

    warning_ids = fields.One2many(
        comodel_name="gc.warning",
        inverse_name="user_id",
    )
    current_warning_id = fields.Many2one(
        comodel_name="gc.warning", compute="_compute_current_warning"
    )
    warning_points = fields.Integer(compute="_compute_warning_points")
    ban_expiration_datetime = fields.Datetime(compute="_compute_ban_time")

    def _compute_current_warning(self):
        for rec in self:
            rec.current_warning_id = first(
                rec.warning_ids.sorted("create_date", reverse=True)
            )

    def _compute_ban_time(self):
        for rec in self:
            current_warning = rec.current_warning_id
            if not current_warning:
                rec.ban_expiration_datetime = False
                continue
            rec.ban_expiration_datetime = current_warning.create_date + timedelta(
                seconds=current_warning.ban_time * 60 * 60
            )

    def _compute_warning_points(self):
        for rec in self:
            rec.warning_points = sum(rec.warning_ids.mapped("points"))

    @api.model
    def get_player_warning_points(self, mc_uuid):
        user = self.search([("mc_uuid", "=", mc_uuid)], limit=1)
        return user.warning_points

    @api.model
    def get_banned_players(self) -> list:
        return [
            {"ban_expiration_datetime": x.ban_expiration_datetime, "mc_uuid": x.mc_uuid}
            for x in self.env["gc.user"].search(
                [("ban_expiration_datetime", "<=", datetime.now())]
            )
        ]
