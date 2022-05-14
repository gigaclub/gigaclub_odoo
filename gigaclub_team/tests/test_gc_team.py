from odoo.tests import SavepointCase


class TestGCTeam(SavepointCase):
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
            }
        )

    def test_create_team(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        user2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
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
                                            "gigaclub_team.gc_permission_model_entry_gc_team_create_team"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        res = GCTeam.create_team("test2", "Test2")
        self.assertEqual(res, 0, "res should be 0")
        team = GCTeam.search([("name", "=", "Test2")])
        self.assertTrue(team, "Team should exist")
        self.assertEqual(
            team.permission_connector_ids.user_id,
            user2,
            "Team should have user2 as manager",
        )
        GCUser.create(
            {
                "name": "Test3",
                "mc_uuid": "test3",
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
                                            "gigaclub_team.gc_permission_model_entry_gc_team_create_team"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        res = GCTeam.create_team("test3", "Test2")
        self.assertEqual(res, 2, "res should be 2")
        GCUser.create(
            {
                "name": "Test4",
                "mc_uuid": "test4",
            }
        )
        res = GCTeam.create_team("test4", "Test2")
        self.assertEqual(res, 3, "res should be 3")

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
                                "permission_profile_entry_template_ids": [
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
        res = GCTeam.edit_team("test", "Test", "test2", "description")
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
                                    "gigaclub_team.gc_permission_profile_template_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.edit_team("test2", "Test", "test3", "description")
        self.assertEqual(res, 1, "res should be 1")

    def test_leave_team(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        self.user.permission_profile_ids = [
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
                            "permission_profile_entry_template_ids": [
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
                                    "gigaclub_team.gc_permission_profile_template_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.leave_team("test", "Test")
        self.assertEqual(res, 0, "res should be 0")
        self.assertFalse(
            self.team.permission_connector_ids,
            "User should not have any permission connectors",
        )
        res = GCTeam.leave_team("test2", "Test")
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
                                    "gigaclub_team.gc_permission_profile_template_default"
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        res = GCTeam.kick_member("test", "Test", "test2")
        self.assertEqual(res, 0, "res should be 0")
        self.assertFalse(
            user_to_kick.permission_connector_ids, "User should not be a member"
        )
        res = GCTeam.kick_member("test", "Test", "test2")
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
        res = GCTeam.kick_member("test", "Test", "test3")
        self.assertEqual(res, 2, "res should be 2")
        self.user.permission_connector_ids = False
        res = GCTeam.kick_member("test", "Test", "test2")
        self.assertEqual(res, 3, "res should be 3")

    # def test_promote_member(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     self.team.manager_ids |= self.user
    #     user_to_promote = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #         }
    #     )
    #     self.team.user_ids |= user_to_promote
    #     res = GCTeam.promote_member("test", "test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     self.assertEqual(
    #         user_to_promote.team_manager_id, self.team, "User should be a manager"
    #     )
    #     team2 = GCTeam.create(
    #         {
    #             "name": "test2",
    #             "description": "test",
    #         }
    #     )
    #     user_to_promote.team_manager_id = False
    #     user_to_promote.team_user_id = team2
    #     res = GCTeam.promote_member("test", "test2")
    #     self.assertEqual(res, 1, "res should be 1")
    #     user_to_promote.team_user_id = False
    #     res = GCTeam.promote_member("test", "test2")
    #     self.assertEqual(res, 2, "res should be 2")
    #     self.user.team_manager_id = False
    #     self.user.team_user_id = self.team
    #     res = GCTeam.promote_member("test", "test2")
    #     self.assertEqual(res, 3, "res should be 3")
    #     self.user.team_user_id = False
    #     res = GCTeam.promote_member("test", "test2")
    #     self.assertEqual(res, 4, "res should be 4")
    #
    # def test_demote_member(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     self.team.manager_ids |= self.user
    #     user_to_demote = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #         }
    #     )
    #     self.team.manager_ids |= user_to_demote
    #     res = GCTeam.demote_member("test", "test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     self.assertFalse(user_to_demote.team_manager_id, "User should not be a manager")
    #     self.assertTrue(user_to_demote.team_user_id, "User should be a member")
    #     team2 = GCTeam.create(
    #         {
    #             "name": "test2",
    #             "description": "test",
    #         }
    #     )
    #     user_to_demote.team_user_id = False
    #     user_to_demote.team_manager_id = team2
    #     res = GCTeam.demote_member("test", "test2")
    #     self.assertEqual(res, 1, "res should be 1")
    #     user_to_demote.team_manager_id = False
    #     user_to_demote.team_user_id = self.team
    #     res = GCTeam.demote_member("test", "test2")
    #     self.assertEqual(res, 2, "res should be 2")
    #     self.user.team_manager_id = False
    #     self.user.team_user_id = self.team
    #     res = GCTeam.demote_member("test", "test2")
    #     self.assertEqual(res, 3, "res should be 3")
    #     self.user.team_user_id = False
    #     res = GCTeam.demote_member("test", "test2")
    #     self.assertEqual(res, 4, "res should be 4")
    #
    # def test_get_team_by_member(self):
    #     GCTeam = self.env["gc.team"]
    #     self.user.team_manager_id = self.team
    #     res = GCTeam.get_team_by_member("test")
    #     self.assertTrue(res, "res should be True")
    #     self.user.team_manager_id = False
    #     self.user.team_user_id = self.team
    #     res = GCTeam.get_team_by_member("test")
    #     self.assertTrue(res, "res should be True")
    #     self.user.team_user_id = False
    #     res = GCTeam.get_team_by_member("test")
    #     self.assertFalse(res, "res should be False")
    #
    # def test_get_all_teams(self):
    #     GCTeam = self.env["gc.team"]
    #     res = GCTeam.get_all_teams()
    #     self.assertTrue(res, "res should be True")
    #     self.team.unlink()
    #     res = GCTeam.get_all_teams()
    #     self.assertFalse(res, "res should be False")
    #
    # def test_get_team(self):
    #     GCTeam = self.env["gc.team"]
    #     res = GCTeam.get_team("test")
    #     self.assertTrue(res, "res should be True")
    #     res = GCTeam.get_team("test2")
    #     self.assertFalse(res, "res should be False")
    #
    # def test_invite_member(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     test2 = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #         }
    #     )
    #     self.team.manager_ids |= self.user
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     self.team.user_ids |= test2
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 1, "res should be 1")
    #     self.team.user_ids = False
    #     self.team.manager_ids |= test2
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 1, "res should be 1")
    #     self.user.team_manager_id = False
    #     self.user.team_user_id = self.team
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 2, "res should be 2")
    #     self.user.team_user_id = False
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 3, "res should be 3")
    #
    # def test_accept_request(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     test2 = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #         }
    #     )
    #     self.team.manager_ids |= self.user
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     res = GCTeam.accept_request("test2", "test")
    #     self.assertEqual(res, 0, "res should be 0")
    #     self.assertEqual(test2.team_user_id, self.team, "test2 should be a member")
    #     res = GCTeam.accept_request("test2", "test")
    #     self.assertEqual(res, 1, "res should be 1")
    #     res = GCTeam.accept_request("test2", "testFALSE")
    #     self.assertEqual(res, 2, "res should be 2")
    #
    # def test_deny_request(self):
    #     GCTeam = self.env["gc.team"]
    #     GCUser = self.env["gc.user"]
    #     test2 = GCUser.create(
    #         {
    #             "name": "Test2",
    #             "mc_uuid": "test2",
    #         }
    #     )
    #     self.team.manager_ids |= self.user
    #     res = GCTeam.invite_member("test", "test2")
    #     self.assertEqual(res, 0, "res should be 0")
    #     res = GCTeam.deny_request("test2", "test")
    #     self.assertEqual(res, 0, "res should be 0")
    #     self.assertNotEqual(
    #         test2.team_user_id, self.team, "test2 should be not a member"
    #     )
    #     res = GCTeam.deny_request("test2", "test")
    #     self.assertEqual(res, 1, "res should be 1")
    #     res = GCTeam.deny_request("test2", "testFALSE")
    #     self.assertEqual(res, 2, "res should be 2")
