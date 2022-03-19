from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestGCBuilderWorld(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attachment = cls.env["ir.attachment"].create(
            {
                "name": "test",
            }
        )
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
        cls.gc_team = cls.env["gc.team"].create(
            {
                "name": "team",
                "user_ids": [(6, 0, [cls.gc_user.id])],
                "manager_ids": [(6, 0, [cls.gc_user_manager.id])],
            }
        )
        cls.gc_team_manager = cls.env["gc.team"].create(
            {
                "name": "team_manager",
                "user_ids": [(6, 0, [cls.gc_user.id])],
                "manager_ids": [(6, 0, [cls.gc_user_manager.id])],
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
                "world_attachment_id": cls.attachment.id,
                "team_ids": [(6, 0, [cls.gc_team.id])],
                "team_manager_ids": [(6, 0, [cls.gc_team_manager.id])],
                "user_ids": [(6, 0, [cls.gc_user.id])],
                "user_manager_ids": [(6, 0, [cls.gc_user_manager.id])],
                "task_id": cls.project_task.id,
            }
        )

    def test__check_user_and_managers(self):
        with self.assertRaises(ValidationError):
            self.gc_builder_world.user_manager_ids |= self.gc_user

    def test__check_teams_and_team_managers(self):
        with self.assertRaises(ValidationError):
            self.gc_builder_world.team_manager_ids |= self.gc_team

    def test_create_as_user(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
            task_id=self.project_task.id,
            name="Test World",
            world_type="normal",
        )
        self.assertTrue(isinstance(res, int))
        gc_builder_world = GCBuilderWorld.browse(res)
        self.assertTrue(gc_builder_world)
        self.assertEqual(gc_builder_world.name, "Test World")
        self.assertEqual(
            gc_builder_world.world_type_id,
            self.env["gc.builder.world.type"].search([("name", "=", "normal")]),
        )
        self.assertEqual(gc_builder_world.task_id, self.project_task)
        self.assertEqual(gc_builder_world.user_manager_ids, self.gc_user)

    def test_create_as_team(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.create_as_team(
            player_uuid="123",
            task_id=self.project_task.id,
            name="Test World",
            world_type="normal",
        )
        self.assertTrue(isinstance(res, int))
        gc_builder_world = GCBuilderWorld.browse(res)
        self.assertTrue(gc_builder_world)
        self.assertEqual(gc_builder_world.name, "Test World")
        self.assertEqual(
            gc_builder_world.world_type_id,
            self.env["gc.builder.world.type"].search([("name", "=", "normal")]),
        )
        self.assertEqual(gc_builder_world.task_id, self.project_task)
        self.assertEqual(gc_builder_world.team_manager_ids, self.gc_team_manager)

    def test_add_user_to_world(self):
        user_to_add = self.env["gc.user"].create(
            {
                "name": "user_to_add",
                "mc_uuid": "321",
            }
        )
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.add_user_to_world(
            player_uuid="456",
            player_uuid_to_add="321",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 0)
        self.assertEqual(self.gc_builder_world.user_ids, self.gc_user | user_to_add)
        self.gc_team_manager.user_ids -= self.gc_user
        res = GCBuilderWorld.add_user_to_world(
            player_uuid="123",
            player_uuid_to_add="321",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 1)
        res = GCBuilderWorld.add_user_to_world(
            player_uuid="123", player_uuid_to_add="321", world_id=0
        )
        self.assertEqual(res, 2)
