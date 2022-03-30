from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    gc_user_ids = fields.Many2many(comodel_name="gc.user")
    gc_team_ids = fields.Many2many(comodel_name="gc.team")

    def return_task(self, task):
        return {
            "id": task.id,
            "name": task.name,
            "description": task.description,
        }

    @api.model
    def get_all_tasks(self):
        return [self.return_task(x) for x in self.search([])]

    @api.model
    def get_task(self, t_id):
        task_id = self.browse(t_id)
        if task_id:
            return self.return_task(task_id)
        return []
