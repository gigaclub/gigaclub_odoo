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

    def action_github_team_user_from_team(self):
        self.ensure_one()
        action = (
            self.sudo()
            .env.ref("github_connector.action_github_team_partner_from_team")
            .read()[0]
        )
        action["context"] = dict(self.env.context)
        action["context"].pop("group_by", None)
        action["context"]["search_default_user_id"] = self.id
        return action
