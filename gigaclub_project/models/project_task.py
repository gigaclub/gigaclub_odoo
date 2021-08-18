from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    gc_user_ids = fields.Many2many(comodel_name="gc.user")
    gc_team_ids = fields.Many2many(comodel_name="gc.team")
