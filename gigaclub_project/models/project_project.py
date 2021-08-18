from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_id = fields.Many2one(required=False)
