from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    # TODO set constraint that this parameter need to be same
    build_width = fields.Integer(default=0)
    build_length = fields.Integer(default=0)

    world_ids = fields.One2many(comodel_name="gc.builder.world", inverse_name="task_id")

    @api.depends("world_ids.permission_connector_ids.user_id")
    def _compute_user_ids(self):
        for task in self.filtered("world_ids.permission_connector_ids.user_id"):
            task.gc_user_ids = task.world_ids.mapped("permission_connector_ids.user_id")

    @api.depends("world_ids.permission_connector_ids.team_id")
    def _compute_team_ids(self):
        for task in self.filtered("world_ids.permission_connector_ids.team_id"):
            task.gc_team_ids = task.world_ids.mapped("permission_connector_ids.team_id")

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
