from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_task = cls.env["project.task"].create(
            {
                "name": "task",
            }
        )
        cls.gc_builder_world = cls.env["gc.builder.world"].create(
            {
                "name": "Test World",
                "task_id": cls.project_task.id,
            }
        )
        cls.project_task_manager = cls.env["project.task"].create(
            {
                "name": "task_manager",
            }
        )
        cls.gc_builder_world_manager = cls.env["gc.builder.world"].create(
            {
                "name": "Test World Manager",
                "task_id": cls.project_task_manager.id,
            }
        )

    def test__check_team_user_manager_id(self):
        GCUser = self.env["gc.user"]
        gc_user = GCUser.create(
            {
                "name": "Test User",
                "world_ids": [(6, 0, [self.gc_builder_world.id])],
            }
        )
        with self.assertRaises(ValidationError):
            gc_user.world_manager_ids = [(6, 0, [self.gc_builder_world.id])]
        gc_user.world_manager_ids = [(6, 0, [self.gc_builder_world_manager.id])]
