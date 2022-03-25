from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestGCLanguage(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test__check_default(self):
        with self.assertRaises(ValidationError):
            self.env["gc.language"].create(
                {
                    "name": "Test",
                    "default": True,
                }
            )
