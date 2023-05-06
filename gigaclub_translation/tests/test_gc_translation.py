from odoo.tests import TransactionCase


class TestGCTranslation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test User",
                "mc_uuid": "test",
                "lang": "en_US",
            }
        )
        cls.translation = cls.env["gc.translation"].create(
            {
                "name": "Test Translation",
            }
        )
        cls.translation_entry = cls.env["gc.translation.entry"].create(
            {
                "translation_ids": [[6, 0, [cls.translation.id]]],
                "lang": "en_US",
                "content": "Test Content",
            }
        )

    def test_get_translation_by_player_uuid(self):
        GCTranslation = self.env["gc.translation"]
        res = GCTranslation.get_translation_by_player_uuid("Test Translation", "test")
        self.assertEqual(res, "Test Content")
        res = GCTranslation.get_translation_by_player_uuid("New Translation", "test")
        self.assertEqual(res, "New Translation")
        res = GCTranslation.get_translation_by_player_uuid(
            "New Translation with Category", "test", category="test_category"
        )
        self.assertEqual(res, "New Translation with Category")
        self.assertEqual(
            self.env["gc.translation"]
            .search([("name", "=", "New Translation with Category")], limit=1)
            .category,
            "test_category",
        )
