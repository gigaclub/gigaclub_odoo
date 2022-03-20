from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    build_width = fields.Integer(default=0)
    build_length = fields.Integer(default=0)

    world_ids = fields.One2many(comodel_name="gc.builder.world", inverse_name="task_id")

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
