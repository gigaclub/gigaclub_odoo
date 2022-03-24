from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestGCUser(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["gc.user"].create(
            {
                "name": "Test",
                "mc_uuid": "test",
            }
        )
        cls.team = cls.env["gc.team"].create(
            {
                "name": "Test",
            }
        )

    def test__check_team_user_manager_id(self):
        self.user.team_manager_id = self.team
        with self.assertRaises(ValidationError):
            self.user.team_user_id = self.team
        self.user.team_manager_id = False

        self.user.team_user_id = self.team
        with self.assertRaises(ValidationError):
            self.user.team_manager_id = self.team
