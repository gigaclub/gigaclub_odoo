from odoo.tests import TransactionCase


class TestGCBuilderWorld(TransactionCase):
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
                "owner_id": cls.gc_user_manager.id,
                "permission_connector_ids": [
                    (
                        0,
                        0,
                        {
                            "user_id": cls.gc_user_manager.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "user_id": cls.gc_user.id,
                            "permission_profile_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "permission_profile_entry_template_ids": [
                                            (
                                                0,
                                                0,
                                                {
                                                    "permission_model_entry_id": cls.env.ref(
                                                        "gigaclub_builder_system.gc_permission_model_entry_gc_team_create_world_as_team"  # noqa: B950
                                                    ).id,
                                                },
                                            )
                                        ],
                                    },
                                )
                            ],
                        },
                    ),
                ],
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
                "owner_id": cls.gc_user_manager.id,
                "permission_connector_ids": [
                    (
                        0,
                        0,
                        {
                            "team_id": cls.gc_team.id,
                        },
                    )
                ],
                "task_id": cls.project_task.id,
            }
        )

    def test_create_as_user(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        self.gc_user.permission_profile_ids = self.env["gc.permission.profile"].create(
            {
                "permission_profile_entry_ids": [
                    (
                        0,
                        0,
                        {
                            "permission_model_entry_id": self.env.ref(
                                "gigaclub_builder_system.gc_permission_model_entry_gc_builder_system_create_world"  # noqa: B950
                            ).id,
                        },
                    )
                ],
            },
        )
        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
            task_id=self.project_task.id,
            name="Test World2",
            world_type_name="normal",
        )
        self.assertEqual(res, 0)
        gc_builder_world = GCBuilderWorld.search(
            [("name", "=", "Test World2")], limit=1
        )
        self.assertTrue(gc_builder_world)
        self.assertEqual(gc_builder_world.name, "Test World2")
        self.assertEqual(
            gc_builder_world.world_type_id,
            self.env["gc.builder.world.type"].search([("name", "=", "normal")]),
        )
        self.assertEqual(gc_builder_world.task_id, self.project_task)
        self.assertEqual(gc_builder_world.owner_id, self.gc_user)
        self.assertTrue(
            self.gc_user in gc_builder_world.permission_connector_ids.mapped("user_id")
        )

        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
            task_id=self.project_task.id,
            name="Test World3",
            world_type_name="",
        )
        self.assertEqual(res, 0)
        gc_builder_world = GCBuilderWorld.search(
            [("name", "=", "Test World3")], limit=1
        )
        self.assertTrue(gc_builder_world)
        self.assertEqual(gc_builder_world.name, "Test World3")
        self.assertEqual(
            gc_builder_world.world_type_id,
            self.env["gc.builder.world.type"].search([("default", "=", True)], limit=1),
        )
        self.assertEqual(gc_builder_world.task_id, self.project_task)
        self.assertEqual(gc_builder_world.owner_id, self.gc_user)
        self.assertTrue(
            self.gc_user in gc_builder_world.permission_connector_ids.mapped("user_id")
        )

        self.gc_user.permission_profile_ids = False
        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
            task_id=self.project_task.id,
            name="Test World2",
            world_type_name="",
        )
        self.assertEqual(res, 1)

    def test_create_as_team(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.create_as_team(
            player_uuid="123",
            team_id=self.gc_team.id,
            task_id=self.project_task.id,
            name="Test World",
            world_type_name="normal",
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
        self.assertEqual(gc_builder_world.owner_id, self.gc_user)
        self.assertTrue(
            self.gc_user in gc_builder_world.permission_connector_ids.mapped("user_id")
        )
        self.assertTrue(
            gc_builder_world.permission_connector_ids.filtered(
                lambda x: x.user_id == self.gc_user
            ).bound_to_team
        )
        self.assertTrue(
            self.gc_team in gc_builder_world.permission_connector_ids.mapped("team_id")
        )

        res = GCBuilderWorld.create_as_team(
            player_uuid="123",
            team_id=self.gc_team.id,
            task_id=self.project_task.id,
            name="Test World",
            world_type_name="",
        )
        self.assertTrue(isinstance(res, int))
        gc_builder_world = GCBuilderWorld.browse(res)
        self.assertTrue(gc_builder_world)
        self.assertEqual(gc_builder_world.name, "Test World")
        self.assertEqual(
            gc_builder_world.world_type_id,
            self.env["gc.builder.world.type"].search([("default", "=", True)], limit=1),
        )
        self.assertEqual(gc_builder_world.task_id, self.project_task)
        self.assertEqual(gc_builder_world.owner_id, self.gc_user)
        self.assertTrue(
            self.gc_user in gc_builder_world.permission_connector_ids.mapped("user_id")
        )
        self.assertTrue(
            gc_builder_world.permission_connector_ids.filtered(
                lambda x: x.user_id == self.gc_user
            ).bound_to_team
        )
        self.assertTrue(
            self.gc_team in gc_builder_world.permission_connector_ids.mapped("team_id")
        )

    def test_remove_user_from_world(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.remove_user_from_world(
            player_uuid="456",
            player_uuid_to_remove="123",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 0)
        self.assertTrue(
            self.gc_user
            not in self.gc_builder_world.permission_connector_ids.mapped("user_id")
        )
        res = GCBuilderWorld.remove_user_from_world(
            player_uuid="123",
            player_uuid_to_remove="456",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 1)

    def test_remove_team_from_world(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.remove_team_from_world(
            player_uuid="456",
            team_id=self.gc_team.id,
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 0)
        self.assertTrue(
            self.gc_team
            not in self.gc_builder_world.permission_connector_ids.mapped("team_id")
        )
        res = GCBuilderWorld.remove_team_from_world(
            player_uuid="456",
            team_id=9999,
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 1)
        res = GCBuilderWorld.remove_team_from_world(
            player_uuid="123",
            team_id=self.gc_team.id,
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 2)

    def test_save_world(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.save_world(
            player_uuid="456",
            world_id=self.gc_builder_world.id,
            world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
        )
        self.assertEqual(res, 0)
        self.assertEqual(
            self.gc_builder_world.world_attachment_id.datas,
            b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
        )
        res = GCBuilderWorld.save_world(
            player_uuid="123", world_id=0, world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA=="
        )
        self.assertEqual(res, 1)

    def test_edit_world_type(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        GCBuilderWorldType = self.env["gc.builder.world.type"]
        res = GCBuilderWorld.edit_world_type(
            player_uuid="456",
            world_id=self.gc_builder_world.id,
            world_type_name="nether",
        )
        self.assertEqual(res, 0)
        self.assertEqual(
            self.gc_builder_world.world_type_id,
            GCBuilderWorldType.search([("name", "=", "nether")], limit=1),
        )
        res = GCBuilderWorld.edit_world_type(
            player_uuid="123", world_id=0, world_type_name="nether"
        )
        self.assertEqual(res, 1)

    def test_get_world_data(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.save_world(
            player_uuid="456",
            world_id=self.gc_builder_world.id,
            world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
        )
        self.assertEqual(res, 0)
        self.assertEqual(
            self.gc_builder_world.world_attachment_id.datas,
            b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
        )
        res = GCBuilderWorld.get_world_data(world_id=self.gc_builder_world.id)
        self.assertEqual(res, b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==")

    def test_get_all_worlds(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.get_all_worlds()
        self.assertEqual(res, [GCBuilderWorld.return_world(self.gc_builder_world)])

    def test_get_world(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.get_world(world_id=self.gc_builder_world.id)
        self.assertEqual(res, GCBuilderWorld.return_world(self.gc_builder_world))
