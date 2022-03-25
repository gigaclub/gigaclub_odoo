from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test User",
                "mc_uuid": "test",
            }
        )

    def test_set_language(self):
        GCUser = self.env["gc.user"]
        res = GCUser.set_language(self.user.mc_uuid, "english")
        self.assertEqual(res, True)
        self.assertEqual(
            self.user.language_id,
            self.env["gc.language"].search([("name", "=", "English")]),
        )
        res = GCUser.set_language(self.user.mc_uuid, "bla")
        self.assertEqual(res, False)
        self.assertEqual(
            self.user.language_id,
            self.env["gc.language"].search([("name", "=", "English")]),
        )
