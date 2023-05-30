from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    reward_id = fields.Many2one(comodel_name="gc.reward")
