from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestGCBuilderWorldType(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test__check_default(self):
        with self.assertRaises(ValidationError):
            self.env["gc.builder.world.type"].create({"name": "Test", "default": True})

    def test_get_all_world_types(self):
        GCBuilderWorldType = self.env["gc.builder.world.type"]
        self.assertEqual(
            GCBuilderWorldType.get_all_world_types(),
            [
                {"id": x.id, "name": x.name, "default": x.default}
                for x in GCBuilderWorldType.search([])
            ],
        )
