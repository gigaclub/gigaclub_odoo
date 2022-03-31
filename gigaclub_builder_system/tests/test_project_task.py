from odoo.tests import SavepointCase


class TestProjectTask(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "description": "Test Task Description",
                "build_width": "10",
                "build_length": "10",
            }
        )
        cls.gc_builder_world = cls.env["gc.builder.world"].create(
            {
                "name": "Test Builder World",
                "task_id": cls.project_task.id,
            }
        )
        cls.gc_user = cls.env["gc.user"].create(
            {
                "name": "Test User",
            }
        )
        cls.gc_team = cls.env["gc.team"].create(
            {
                "name": "Test Team",
            }
        )

    def test_return_task(self):
        ProjectTask = self.env["project.task"]
        res = ProjectTask.return_task(self.project_task)
        self.assertTrue(res)
        self.assertTrue("build_width" in res)
        self.assertTrue("build_length" in res)
        self.assertTrue("world_ids" in res)

    def test__compute_gc_user_ids(self):
        self.gc_builder_world.user_ids |= self.gc_user
        self.assertTrue(self.gc_user in self.project_task.gc_user_ids)

    def test__compute_gc_team_ids(self):
        self.gc_builder_world.team_ids |= self.gc_team
        self.assertTrue(self.gc_team in self.project_task.gc_team_ids)
