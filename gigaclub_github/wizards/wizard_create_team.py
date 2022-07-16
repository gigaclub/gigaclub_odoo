from odoo import fields, models


class WizardCreateTeam(models.TransientModel):
    _inherit = "wizard.create.team"

    wizard_user_ids = fields.Many2many(
        string="Team Members",
        comodel_name="gc.user",
        domain="[('github_name', '!=', False)]",
    )

    def get_github_data_from_odoo(self):
        self.ensure_one()
        res = super().get_github_data_from_odoo()
        res.update(
            {
                "maintainers": [
                    x.github_name for x in self.wizard_user_ids if x.github_name
                ],
            }
        )
        return res
