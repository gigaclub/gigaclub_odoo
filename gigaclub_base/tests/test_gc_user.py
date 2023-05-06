from psycopg2.errors import UniqueViolation

from odoo.tests import TransactionCase


class TestGCUser(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gc_user = cls.env["gc.user"].create(
            {
                "name": "test",
                "mc_uuid": "12345",
            }
        )

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
