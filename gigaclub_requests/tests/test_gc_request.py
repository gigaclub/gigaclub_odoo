from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestGCRequest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test User",
                "mc_uuid": "test",
            }
        )

    def test__check_duplicate_request(self):
        self.env["gc.request"].create(
            {
                "receiver_id": f"gc.user,{self.user.id}",
                "sender_id": f"gc.user,{self.user.id}",
                "state": "waiting",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["gc.request"].create(
                {
                    "receiver_id": f"gc.user,{self.user.id}",
                    "sender_id": f"gc.user,{self.user.id}",
                    "state": "waiting",
                }
            )
