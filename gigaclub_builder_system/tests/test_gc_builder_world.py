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
        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
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

        res = GCBuilderWorld.create_as_user(
            player_uuid="123",
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

    def test_create_as_team(self):
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.create_as_team(
            player_uuid="123",
            team="team",
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
            team="team",
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
        self.assertTrue(
            user_to_add
            in self.gc_builder_world.permission_connector_ids.mapped("user_id")
        )
        self.gc_builder_world.owner_id = user_to_add
        res = GCBuilderWorld.add_user_to_world(
            player_uuid="123",
            player_uuid_to_add="321",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 1)

    def test_add_team_to_world(self):
        user_to_add = self.env["gc.user"].create(
            {
                "name": "user_to_add",
                "mc_uuid": "321",
            }
        )
        team_to_add = self.env["gc.team"].create(
            {
                "name": "team_to_add",
                "owner_id": user_to_add.id,
                "permission_connector_ids": [
                    (
                        0,
                        0,
                        {
                            "user_id": user_to_add.id,
                        },
                    ),
                ],
            }
        )
        GCBuilderWorld = self.env["gc.builder.world"]
        res = GCBuilderWorld.add_team_to_world(
            player_uuid="456",
            team_name="team_to_add",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 0)
        self.assertTrue(
            team_to_add
            in self.gc_builder_world.permission_connector_ids.mapped("team_id")
        )
        self.assertTrue(
            user_to_add
            in self.gc_builder_world.permission_connector_ids.mapped("user_id")
        )
        res = GCBuilderWorld.add_team_to_world(
            player_uuid="456",
            team_name="bla",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 1)
        res = GCBuilderWorld.add_team_to_world(
            player_uuid="123",
            team_name="team_to_add",
            world_id=self.gc_builder_world.id,
        )
        self.assertEqual(res, 2)

    #
    # def test_remove_user_from_world(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.remove_user_from_world(
    #         player_uuid="456",
    #         player_uuid_to_remove="123",
    #         world_id=self.gc_builder_world.id,
    #     )
    #     self.assertEqual(res, 0)
    #     self.assertTrue(self.gc_user not in self.gc_builder_world.user_ids)
    #     self.gc_team_manager.user_ids -= self.gc_user
    #     res = GCBuilderWorld.remove_user_from_world(
    #         player_uuid="123",
    #         player_uuid_to_remove="456",
    #         world_id=self.gc_builder_world.id,
    #     )
    #     self.assertEqual(res, 1)
    #     res = GCBuilderWorld.remove_user_from_world(
    #         player_uuid="123", player_uuid_to_remove="456", world_id=0
    #     )
    #     self.assertEqual(res, 2)
    #
    # def test_remove_team_from_world(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.remove_team_from_world(
    #         player_uuid="456",
    #         team_name="team",
    #         world_id=self.gc_builder_world.id,
    #     )
    #     self.assertEqual(res, 0)
    #     self.assertTrue(self.gc_team not in self.gc_builder_world.team_ids)
    #     res = GCBuilderWorld.remove_team_from_world(
    #         player_uuid="456",
    #         team_name="bla",
    #         world_id=self.gc_builder_world.id,
    #     )
    #     self.assertEqual(res, 1)
    #     self.gc_team_manager.user_ids -= self.gc_user
    #     res = GCBuilderWorld.remove_team_from_world(
    #         player_uuid="123", team_name="team", world_id=self.gc_builder_world.id
    #     )
    #     self.assertEqual(res, 2)
    #     res = GCBuilderWorld.remove_team_from_world(
    #         player_uuid="123", team_name="team", world_id=0
    #     )
    #     self.assertEqual(res, 3)
    #
    # def test_save_world(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.save_world(
    #         world_id=self.gc_builder_world.id,
    #         world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
    #     )
    #     self.assertEqual(res, 0)
    #     self.assertEqual(
    #         self.gc_builder_world.world_attachment_id.datas,
    #         b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
    #     )
    #     res = GCBuilderWorld.save_world(
    #         world_id=0, world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA=="
    #     )
    #     self.assertEqual(res, 1)
    #
    # def test_edit_world_type(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     GCBuilderWorldType = self.env["gc.builder.world.type"]
    #     res = GCBuilderWorld.edit_world_type(
    #         world_id=self.gc_builder_world.id, world_type="nether"
    #     )
    #     self.assertEqual(res, 0)
    #     self.assertEqual(
    #         self.gc_builder_world.world_type_id,
    #         GCBuilderWorldType.search([("name", "=", "nether")], limit=1),
    #     )
    #     res = GCBuilderWorld.edit_world_type(world_id=0, world_type="nether")
    #     self.assertEqual(res, 1)
    #
    # def test_get_world_data(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.save_world(
    #         world_id=self.gc_builder_world.id,
    #         world_data="YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
    #     )
    #     self.assertEqual(res, 0)
    #     self.assertEqual(
    #         self.gc_builder_world.world_attachment_id.datas,
    #         b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==",
    #     )
    #     res = GCBuilderWorld.get_world_data(world_id=self.gc_builder_world.id)
    #     self.assertEqual(res, b"YXNzYWRhc2Rkc2RzYXNhZHNhZGFzZA==")
    #
    # def test_get_all_worlds(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.get_all_worlds()
    #     self.assertEqual(res, [GCBuilderWorld.return_world(self.gc_builder_world)])
    #
    # def test_get_world(self):
    #     GCBuilderWorld = self.env["gc.builder.world"]
    #     res = GCBuilderWorld.get_world(w_id=self.gc_builder_world.id)
    #     self.assertEqual(res, GCBuilderWorld.return_world(self.gc_builder_world))
