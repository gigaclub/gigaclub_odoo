from odoo import fields, models


class GCExperience(models.Model):
    _name = "gc.experience"
    _description = "GigaClub Experience"

    name = fields.Char()
    level_ids = fields.One2many(
        comodel_name="gc.experience.level", inverse_name="experience_id"
    )
