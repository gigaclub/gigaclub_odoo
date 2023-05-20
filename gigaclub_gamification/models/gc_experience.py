from odoo import fields, models


class GCExperience(models.Model):
    _name = "gc.experience"
    _description = "GigaClub Experience"

    name = fields.Char()
