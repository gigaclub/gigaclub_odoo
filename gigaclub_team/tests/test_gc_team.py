from odoo.tests import TransactionCase


class TestGCTeam(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test",
                "mc_uuid": "test",
            }
        )
        cls.team = cls.env["gc.team"].create(
            {
                "name": "Test",
                "owner_id": cls.user.id,
            }
        )

    # def test_create_team(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     user2 = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #             "permission_profile_ids": [
    #                 (
    #                     0,
    #                     0,
    #                     {
    #                         "permission_profile_entry_ids": [
    #                             (
    #                                 0,
    #                                 0,
    #                                 {
    #                                     "permission_model_entry_id": self.env.ref(
    #                                         "gigaclub_team.gc_permission_model_entry_gc_team_create_team"  # noqa: B950
    #                                     ).id,
    #                                 },
    #                             )
    #                         ],
    #                     },
    #                 )
    #             ],
    #         }
    #     )
    #     res = GCTeam.create_team("test2", "Test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     team = GCTeam.search([("name", "=", "Test2")])
    #     self.assertTrue(team, "Team should exist")
    #     self.assertEqual(
    #         team.permission_connector_ids.user_id,
    #         user2,
    #         "Team should have user2 as manager",
    #     )
    #     GCUser.create(
    #         {
    #             "name": "Test3",
    #             "mc_uuid": "test3",
    #             "permission_profile_ids": [
    #                 (
    #                     0,
    #                     0,
    #                     {
    #                         "permission_profile_entry_ids": [
    #                             (
    #                                 0,
    #                                 0,
    #                                 {
    #                                     "permission_model_entry_id": self.env.ref(
    #                                         "gigaclub_team.gc_permission_model_entry_gc_team_create_team"  # noqa: B950
    #                                     ).id,
    #                                 },
    #                             )
    #                         ],
    #                     },
    #                 )
    #             ],
    #         }
    #     )
    #     res = GCTeam.create_team("test3", "Test2")
    #     self.assertEqual(res, 2, "res should be 2")
    #     GCUser.create(
    #         {
    #             "name": "Test4",
    #             "mc_uuid": "test4",
    #         }
    #     )
    #     res = GCTeam.create_team("test4", "Test2")
    #     self.assertEqual(res, 3, "res should be 3")

    def test_edit_team(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_entry_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_edit_team"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.edit_team("test", self.team.id, "test2", "description")
        self.assertEqual(res, 0, "res should be 0")
        self.assertEqual(self.team.name, "test2", "Team name should be test2")
        self.assertEqual(
            self.team.description,
            "description",
            "Team description should be description",
        )
        user2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": user2.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.edit_team("test2", self.team.id, "test3", "description")
        self.assertEqual(res, 1, "res should be 1")

    def test_leave_team(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        self.user.permission_profile_ids = [
            (
                0,
                0,
                {
                    "permission_profile_entry_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_model_entry_id": self.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_leave_team"  # noqa: B950
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
                "permission_profile_ids": [
                    (
                        0,
                        0,
                        {
                            "permission_profile_entry_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "permission_model_entry_id": self.env.ref(
                                            "gigaclub_team.gc_permission_model_entry_gc_team_leave_team"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.leave_team("test", self.team.id)
        self.assertEqual(res, 0, "res should be 0")
        self.assertFalse(
            self.team.permission_connector_ids,
            "User should not have any permission connectors",
        )
        res = GCTeam.leave_team("test2", self.team.id)
        self.assertEqual(res, 1, "res should be 1")

    def test_kick_member(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
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
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        user_to_kick = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": user_to_kick.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.kick_member("test", self.team.id, "test2")
        self.assertEqual(res, 0, "res should be 0")
        self.assertFalse(
            user_to_kick.permission_connector_ids, "User should not be a member"
        )
        res = GCTeam.kick_member("test", self.team.id, "test2")
        self.assertEqual(res, 1, "res should be 1")
        self.user.permission_connector_ids = False
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_entry_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.kick_member("test", self.team.id, "test3")
        self.assertEqual(res, 3, "res should be 3")
        self.user.permission_connector_ids = False
        res = GCTeam.kick_member("test4", self.team.id, "test2")
        self.assertEqual(res, 4, "res should be 4")

    # def test_get_teams_by_member(self):
    #     GCTeam = self.env["gc.team"]
    #     self.team.permission_connector_ids = [
    #         (
    #             0,
    #             0,
    #             {
    #                 "user_id": self.user.id,
    #                 "permission_profile_ids": [
    #                     (
    #                         0,
    #                         0,
    #                         {
    #                             "permission_profile_entry_ids": [
    #                                 (
    #                                     0,
    #                                     0,
    #                                     {
    #                                         "permission_model_entry_id": self.env.ref(
    #                                             "gigaclub_team.gc_permission_model_entry_gc_team_kick_member"  # noqa: B950
    #                                         ).id,
    #                                     },
    #                                 )
    #                             ],
    #                         },
    #                     )
    #                 ],
    #             },
    #         )
    #     ]
    #     res = GCTeam.get_teams_by_member("test")
    #     self.assertTrue(res, "res should be True")
    #     self.team.permission_connector_ids = False
    #     res = GCTeam.get_teams_by_member("test")
    #     self.assertFalse(res, "res should be False")

    def test_get_all_teams(self):
        GCTeam = self.env["gc.team"]
        res = GCTeam.get_all_teams()
        self.assertTrue(res, "res should be True")
        self.env["gc.team"].search([]).unlink()
        res = GCTeam.get_all_teams()
        self.assertFalse(res, "res should be False")

    def test_get_team(self):
        GCTeam = self.env["gc.team"]
        res = GCTeam.get_team(self.team.id)
        self.assertTrue(res, "res should be True")
        res = GCTeam.get_team(999)
        self.assertFalse(res, "res should be False")

    def test_invite_member(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        test2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_entry_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.invite_member("test", self.team.id, "test2")
        self.assertEqual(res, 0, "res should be 0")
        res = GCTeam.invite_member("test", self.team.id, "test2")
        self.assertEqual(res, 1, "res should be 1")
        self.env["gc.request"].search([]).unlink()
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": test2.id,
                },
            )
        ]
        res = GCTeam.invite_member("test", self.team.id, "test2")
        self.assertEqual(res, 2, "res should be 2")
        res = GCTeam.invite_member("test", self.team.id, "test2wrongwrong")
        self.assertEqual(res, 3, "res should be 3")
        self.team.permission_connector_ids = False
        res = GCTeam.invite_member("test4", self.team.id, "test2")
        self.assertEqual(res, 4, "res should be 4")

    def test_accept_request(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        test2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
                "permission_group_ids": [
                    (
                        6,
                        0,
                        self.env.ref(
                            "gigaclub_permission_system.gc_permission_group_gigaclub"
                        ).ids,
                    )
                ],
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_entry_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.invite_member("test", self.team.id, "test2")
        self.assertEqual(res, 0, "res should be 0")
        test2.permission_profile_ids = [
            (
                0,
                0,
                {
                    "permission_profile_entry_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_model_entry_id": self.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_accept_request"  # noqa: B950
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.accept_request("test2", self.team.id)
        self.assertEqual(res, 0, "res should be 0")
        res = GCTeam.accept_request("test2", self.team.id)
        self.assertEqual(res, 1, "res should be 1")
        res = GCTeam.accept_request("test2", 999)
        self.assertEqual(res, 2, "res should be 2")
        test2.permission_profile_ids = False
        test2.permission_group_ids = False
        res = GCTeam.accept_request("test2", self.team.id)
        self.assertEqual(res, 3, "res should be 3")

    def test_deny_request(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        test2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
            }
        )
        self.team.permission_connector_ids = [
            (
                0,
                0,
                {
                    "user_id": self.user.id,
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
                                            "permission_model_entry_id": self.env.ref(
                                                "gigaclub_team.gc_permission_model_entry_gc_team_invite_member"  # noqa: B950
                                            ).id,
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.invite_member("test", self.team.id, "test2")
        self.assertEqual(res, 0, "res should be 0")
        test2.permission_profile_ids = [
            (
                0,
                0,
                {
                    "permission_profile_entry_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_model_entry_id": self.env.ref(
                                    "gigaclub_team.gc_permission_model_entry_gc_team_deny_request"  # noqa: B950
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.deny_request("test2", self.team.id)
        self.assertEqual(res, 0, "res should be 0")
        res = GCTeam.deny_request("test2", self.team.id)
        self.assertEqual(res, 1, "res should be 1")
        res = GCTeam.deny_request("test2", 999)
        self.assertEqual(res, 2, "res should be 2")
        test2.permission_profile_ids = False
        res = GCTeam.deny_request("test2", self.team.id)
        self.assertEqual(res, 3, "res should be 3")
