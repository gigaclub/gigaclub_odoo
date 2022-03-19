from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    def test_method(self):
        res = self.env["gc.user"].test()
        self.assertEqual(res, "test123", "res should be test.")
