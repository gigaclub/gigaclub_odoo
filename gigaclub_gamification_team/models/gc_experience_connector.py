from odoo import fields, models


class GCExperienceConnector(models.Model):
    _inherit = "gc.experience.connector"

    team_id = fields.Many2one(comodel_name="gc.team")
