from odoo.tests import TransactionCase


class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.partner_demo")
        cls.gc_user = cls.env["gc.user"].create(
            {
                "name": "test",
            }
        )

    def test__inverse_name(self):
        self.partner.gc_user_id = self.gc_user
        self.assertEqual(self.partner.gc_user_id.name, "test", "Name should be test")
        self.partner.name = "partnername"
        self.assertEqual(
            self.partner.gc_user_id.name, "partnername", "Name should be partnername"
        )

    def test_name_get(self):
        name = self.partner.name_get()
        self.assertEqual(
            name[0][1], self.partner.name, "Name should be the name of the Partner"
        )
