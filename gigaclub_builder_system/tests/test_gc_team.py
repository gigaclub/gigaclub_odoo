from odoo.tests import SavepointCase


class TestGCTeam(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        GCTeam = cls.env["gc.team"]
        cls.gc_user = cls.env["gc.user"].create(
            {
                "name": "user",
                "mc_uuid": "123",
            }
        )
        cls.gc_user_manager = cls.env["gc.user"].create(
            {
                "name": "manager",
                "mc_uuid": "456",
            }
        )
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
        cls.team = GCTeam.create(
            {
                "name": "Test Team",
                "description": "Test Team Description",
                "user_ids": [(6, 0, [cls.gc_user.id])],
                "manager_ids": [(6, 0, [cls.gc_user_manager.id])],
                "world_ids": [(6, 0, [cls.gc_builder_world.id])],
                "world_manager_ids": [(6, 0, [cls.gc_builder_world_manager.id])],
            }
        )

    def test_return_team(self):
        GCTeam = self.env["gc.team"]
        res = GCTeam.return_team(self.team)
        self.assertTrue(res)
        self.assertTrue("world_ids" in res)
        self.assertTrue("world_manager_ids" in res)
