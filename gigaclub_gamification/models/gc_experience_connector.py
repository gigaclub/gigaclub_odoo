from odoo import fields, models


class GCExperienceConnector(models.Model):
    _name = "gc.experience.connector"
    _description = "GigaClub Experience Connector"

    user_id = fields.Many2one(comodel_name="gc.user")
    experience = fields.Many2one(comodel_name="gc.experience")
    amount = fields.Integer()
