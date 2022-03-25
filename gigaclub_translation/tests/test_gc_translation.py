from odoo.tests import SavepointCase


class TestGCTranslation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.language = cls.env.ref("gigaclub_translation.gc_language_english")
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test User",
                "mc_uuid": "test",
                "language_id": cls.language.id,
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
                "language_id": cls.language.id,
                "content": "Test Content",
            }
        )

    def test_get_translation_by_player_uuid(self):
        GCTranslation = self.env["gc.translation"]
        res = GCTranslation.get_translation_by_player_uuid("Test Translation", "test")
        self.assertEqual(res, "Test Content")
        res = GCTranslation.get_translation_by_player_uuid("New Translation", "test")
        self.assertEqual(res, "New Translation")
