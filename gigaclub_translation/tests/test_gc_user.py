# grepper odoo test savepointcase
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
        res = GCUser.set_language(self.user.mc_uuid, "en_US")
        self.assertEqual(res, True)
        self.assertEqual(
            self.user.lang,
            "en_US",
        )
        res = GCUser.set_language(self.user.mc_uuid, "bla")
        self.assertEqual(res, False)
        self.assertEqual(
            self.user.lang,
            "en_US",
        )


# end grepper
