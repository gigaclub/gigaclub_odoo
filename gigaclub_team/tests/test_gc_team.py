from odoo.exceptions import MissingError
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

    def test__inverse_users(self):
        self.team.user_ids |= self.user
        self.assertEqual(self.team.manager_ids, self.user)
        self.assertFalse(self.team.user_ids)
        self.team.manager_ids -= self.user
        with self.assertRaises(MissingError):
            self.assertFalse(self.team.name)

    def test_create_team(self):
        GCTeam = self.env["gc.team"]
        GCUser = self.env["gc.user"]
        user2 = GCUser.create(
            {
                "name": "Test2",
                "mc_uuid": "test2",
            }
        )
        res = GCTeam.create_team("test2", "Test2")
        self.assertEqual(res, 0, "res should be 0")
        team = GCTeam.search([("name", "=", "Test2")])
        self.assertTrue(team, "Team should exist")
        self.assertEqual(team.manager_ids, user2, "Team should have user2 as manager")
        GCUser.create(
            {
                "name": "Test3",
                "mc_uuid": "test3",
            }
        )
        res = GCTeam.create_team("test3", "Test2")
        self.assertEqual(res, 2, "res should be 2")
        res = GCTeam.create_team("test2", "Test2")
        self.assertEqual(res, 3, "res should be 3")
