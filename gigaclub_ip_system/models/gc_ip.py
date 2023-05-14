from odoo import fields, models


class GigaClubIP(models.Model):
    _name = "gc.ip"
    _description = "GigaClub IP Address"

    ipv4_hash = fields.Char()
    ipv6_hash = fields.Char()  # for later purposes
    blocked = fields.Boolean()

    _sql_constraints = [
        ("ipv4_hash", "UNIQUE(ipv4_hash)", "ipv4_hash must be unique!"),
        ("ipv6_hash", "UNIQUE(ipv6_hash)", "ipv6_hash must be unique!"),
    ]
