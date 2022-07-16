from odoo import api, fields, models


class GitHubTeam(models.Model):
    _inherit = "github.team"

    user_ids = fields.One2many(
        string="Members",
        comodel_name="github.team.user",
        inverse_name="team_id",
        readonly=True,
    )
    user_qty = fields.Integer(
        string="Number of Members", compute="_compute_user_qty", store=True
    )

    @api.depends("user_ids")
    def _compute_user_qty(self):
        for team in self:
            team.user_qty = len(team.user_ids)
