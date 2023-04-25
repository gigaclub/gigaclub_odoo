from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCRequest(models.Model):
    _inherit = "gc.request"

    receiver_id = fields.Reference(selection_add=[("gc.team", "gc.team")])
    sender_id = fields.Reference(selection_add=[("gc.team", "gc.team")])
    request_type = fields.Selection(
        selection_add=[("member_to_team_invitation", "Member to Team invitation")]
    )

    @api.constrains("receiver_id", "sender_id", "request_type")
    def _check_request_type(self):
        for rec in self:
            if rec.request_type == "member_to_team_invitation" and (
                not rec.receiver_id._name == "gc.user"
                or not rec.sender_id._name == "gc.team"
            ):
                raise ValidationError(
                    _(
                        "The receiver needs to be type of "
                        "'gc.user' and the sender type of 'gc.team'!"
                    )
                )

    @api.model
    def get_team_member_to_team_invitations(self, team_id):
        return [
            {
                "receiver_mc_uuid": x.receiver_id.mc_uuid,
                "sender_team_id": x.sender_id.id,
            }
            for x in self.search(
                [
                    ("sender_id", "=", f"gc.team,{team_id}"),
                    ("state", "=", "waiting"),
                    ("request_type", "=", "member_to_team_invitation"),
                ]
            )
        ]

    @api.model
    def get_user_member_to_team_invitations(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        return [
            {
                "receiver_mc_uuid": x.receiver_id.mc_uuid,
                "sender_team_id": x.sender_id.id,
            }
            for x in self.search(
                [
                    ("receiver_id", "=", f"gc.user,{user.id}"),
                    ("state", "=", "waiting"),
                    ("request_type", "=", "member_to_team_invitation"),
                ]
            )
        ]
