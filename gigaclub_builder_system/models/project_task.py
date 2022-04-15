from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    build_width = fields.Integer(default=0)
    build_length = fields.Integer(default=0)

    world_ids = fields.One2many(comodel_name="gc.builder.world", inverse_name="task_id")

    @api.depends("world_ids.user_ids", "world_ids.user_manager_ids")
    def _compute_user_ids(self):
        for task in self.filtered("world_ids"):
            task.user_ids = task.world_ids.mapped("user_ids") | task.world_ids.mapped(
                "user_manager_ids"
            )

    @api.depends("world_ids.team_ids", "world_ids.team_manager_ids")
    def _compute_team_ids(self):
        for task in self.filtered("world_ids"):
            task.team_ids = task.world_ids.mapped("team_ids") | task.world_ids.mapped(
                "team_manager_ids"
            )

    def return_task(self, task):
        res = super().return_task(task)
        res.update(
            {
                "build_width": task.build_width,
                "build_length": task.build_length,
                "world_ids": [{"id": w.id} for w in task.world_ids],
            }
        )
        return res
