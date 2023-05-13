from odoo import fields, models


class GigaClubIP(models.Model):
    _name = "gc.ip"
    _description = "GigaClub IP Address"

    ipv4_hash = fields.Char()
    ipv6_hash = fields.Char()
    blocked = fields.Boolean()
    user_ids = fields.Many2many(comodel_name="gc.user")
