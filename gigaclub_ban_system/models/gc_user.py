from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    warning_ids = fields.One2many(
        comodel_name="gc.warning",
        inverse_name="user_id",
        inverse="_inverse_warning_ids",
    )
    permanent_banned = fields.Boolean()

    def _inverse_warning_ids(self):
        for rec in self:
            if len(rec.warning_ids) > 2:
                rec.permanent_banned = True
                continue
