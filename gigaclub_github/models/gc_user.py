from odoo import api, fields, models


# grepper odoo inherit multiple models
class GCUser(models.Model):
    _name = "gc.user"
    _inherit = ["gc.user", "abstract.github.model"]
    # end grepper

    _github_login_field = "github_name"
    _need_individual_call = True

    github_team_user_ids = fields.One2many(
        string="Teams",
        comodel_name="github.team.user",
        inverse_name="user_id",
        readonly=True,
    )
    github_team_qty = fields.Integer(
        string="Number of Teams", compute="_compute_github_team_qty", store=True
    )
    organization_ids = fields.Many2many(
        string="Organizations",
        comodel_name="github.organization",
        relation="github_organization_user_rel",
        column1="user_id",
        column2="organization_id",
        readonly=True,
    )
    organization_qty = fields.Integer(
        string="Number of Organizations",
        compute="_compute_organization_qty",
        store=True,
    )

    _sql_constraints = [
        (
            "github_login_uniq",
            "unique(github_name)",
            "Two different partners cannot have the same Github Login",
        )
    ]

    @api.depends("organization_ids", "organization_ids.member_ids")
    def _compute_organization_qty(self):
        for user in self:
            user.organization_qty = len(user.organization_ids)

    @api.depends("github_team_user_ids")
    def _compute_github_team_qty(self):
        for user in self:
            user.github_team_qty = len(user.github_team_user_ids)

    def action_github_organization(self):
        self.ensure_one()
        action = (
            self.sudo().env.ref("github_connector.action_github_organization").read()[0]
        )
        action["context"] = dict(self.env.context)
        action["context"].pop("group_by", None)
        action["context"]["search_default_member_ids"] = self.id
        return action

    def action_github_team_partner_from_partner(self):
        self.ensure_one()
        action = (
            self.sudo()
            .env.ref("github_connector.action_github_team_partner_from_partner")
            .read()[0]
        )
        action["context"] = dict(self.env.context)
        action["context"].pop("group_by", None)
        action["context"]["search_default_user_id"] = self.id
        return action
