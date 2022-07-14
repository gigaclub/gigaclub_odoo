from odoo import api, fields, models


class GitHubTeamUser(models.Model):
    _name = "github.team.user"
    _description = "GitHub Team User"
    _order = "team_id,user_id"

    _ROLE_SELECTION = [("member", "Member"), ("maintainer", "Maintainer")]

    team_id = fields.Many2one(
        comodel_name="github.team",
        string="Team",
        required=True,
        index=True,
        readonly=True,
        ondelete="cascade",
    )
    user_id = fields.Many2one(
        comodel_name="gc.user",
        string="Member",
        required=True,
        index=True,
        readonly=True,
        ondelete="cascade",
    )
    role = fields.Selection(
        selection=_ROLE_SELECTION, string="Role", required=True, readonly=True
    )
    context_search_default_team_id = fields.Integer(
        compute="_compute_context_search_default"
    )
    context_search_default_user_id = fields.Integer(
        compute="_compute_context_search_default"
    )

    @api.depends_context("search_default_team_id", "search_default_user_id")
    def _compute_context_search_default(self):
        """Compute the context value for the search terms
        into helper fields for the view
        """
        for record in self:
            record.context_search_default_team_id = self.env.context.get(
                "search_default_team_id", False
            )
            record.context_search_default_user_id = self.env.context.get(
                "search_default_user_id", False
            )
