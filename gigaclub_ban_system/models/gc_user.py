from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    warning_ids = fields.One2many(
        comodel_name="gc.warning",
        inverse_name="user_id",
    )
    warning_points = fields.Integer(compute="_compute_warning_points")

    def _compute_warning_points(self):
        for rec in self:
            rec.warning_points = sum(rec.warning_ids.mapped("points"))
