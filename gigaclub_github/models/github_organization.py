from odoo import fields, models


class GitHubOrganization(models.Model):
    _inherit = "github.organization"

    member_ids = fields.Many2many(
        string="Members",
        comodel_name="gc.user",
        relation="github_organization_user_rel",
        column1="organization_id",
        column2="user_id",
        readonly=True,
    )

    member_qty = fields.Integer(
        string="Number of Members", compute="_compute_member_qty", store=True
    )

    # Action section
    def button_sync_member(self):
        gh_org = self.find_related_github_object()
        user_obj = self.env["gc.user"]
        for organization in self:
            member_ids = []
            for gh_member in gh_org.get_members():
                user = user_obj.get_from_id_or_create(gh_data=gh_member)
                member_ids.append(user.id)
            organization.member_ids = member_ids
