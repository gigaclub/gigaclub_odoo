from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    def test_method(self):
        res = self.env["gc.user"].test()
        self.assertEqual(res, "test1234", "res should be test.")
