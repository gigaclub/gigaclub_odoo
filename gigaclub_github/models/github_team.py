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

    # Action Section
    def button_sync_member(self):
        user_obj = self.env["gc.user"]
        gh_team = self.find_related_github_object()
        for team in self:
            user_data = []
            # Fetching the role after getting each user requires more API calls for
            # each user, so we fetch the users in 2 steps, one for each role
            for gh_user in gh_team.get_members(role="member"):
                user = user_obj.get_from_id_or_create(gh_data=gh_user)
                user_data.append({"user_id": user.id, "role": "member"})
            for gh_user in gh_team.get_members(role="maintainer"):
                user = user_obj.get_from_id_or_create(gh_data=gh_user)
                user_data.append({"user_id": user.id, "role": "maintainer"})
            team.user_ids = [(2, x.id, False) for x in team.user_ids]
            team.user_ids = [(0, False, x) for x in user_data]
