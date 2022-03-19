from psycopg2.errors import UniqueViolation

from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_gc_user_create(self):
        """Check if creating a new user works"""
        GCUser = self.env["gc.user"]
        gc_user_1 = GCUser.create(
            {
                "name": "Test User",
                "state": "online",
                "mc_uuid": "123",
            }
        )
        self.assertEqual(gc_user_1.name, "Test User")
        self.assertEqual(gc_user_1.state, "online")
        self.assertEqual(gc_user_1.mc_uuid, "123")
        # check constraints
        with self.assertRaises(UniqueViolation):
            GCUser.create(
                {
                    "name": "Test User",
                    "state": "online",
                    "mc_uuid": "123",
                }
            )
