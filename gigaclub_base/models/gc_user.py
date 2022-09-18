from odoo import api, fields, models


class GCUser(models.Model):
    _name = "gc.user"
    _description = "GigaClub User"

    name = fields.Char(compute="_compute_name", store=True)
    mc_name = fields.Char()
    mc_uuid = fields.Char(index=True)
    state = fields.Selection(
        selection=[("online", "Online"), ("offline", "Offline")], default="offline"
    )

    _sql_constraints = [
        ("mc_uuid_unique", "UNIQUE(mc_uuid)", "MC_UUID must be unique!")
    ]

    @api.depends("mc_name")
    def _compute_name(self):
        for rec in self:
            rec.name = rec.mc_name

    def name_get(self):
        res = []
        for rec in self:
            if self.env.context.get("mc_name", False):
                res.append((rec.id, f"({rec.name}) - {rec.mc_uuid}"))
            else:
                res.append((rec.id, rec.name))
        return res
