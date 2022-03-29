from odoo import fields, models


class GCUser(models.Model):
    _name = "gc.user"
    _description = "GigaClub User"

    name = fields.Char()
    mc_uuid = fields.Char()
    state = fields.Selection(
        selection=[("online", "Online"), ("offline", "Offline")], default="offline"
    )

    _sql_constraints = [
        ("mc_uuid_unique", "UNIQUE(mc_uuid)", "MC_UUID must be unique!")
    ]

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f"({rec.name}) - {rec.mc_uuid}"))
        return res
