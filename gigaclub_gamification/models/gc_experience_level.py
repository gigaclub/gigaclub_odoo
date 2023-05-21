from odoo import fields, models


class GCExperienceLevel(models.Model):
    _name = "gc.experience.level"
    _description = "GigaClub Experience Level"

    level = fields.Integer()
    experience_id = fields.Many2one(comodel_name="gc.experience", index=True)
    experience_amount = fields.Integer()
