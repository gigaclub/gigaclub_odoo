from odoo import fields, models
from odoo.fields import first


class GCExperienceConnector(models.Model):
    _name = "gc.experience.connector"
    _description = "GigaClub Experience Connector"

    user_id = fields.Many2one(comodel_name="gc.user")
    experience_id = fields.Many2one(comodel_name="gc.experience")
    amount = fields.Integer()
    level_id = fields.Many2one(
        comodel_name="gc.experience.level", compute="_compute_level"
    )

    def _compute_level(self):
        for rec in self:
            rec.level_id = first(
                rec.experience_id.level_ids.filtered(
                    lambda x: x.experience_amount < rec.amount
                )
            )
