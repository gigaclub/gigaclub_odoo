from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCRequest(models.Model):
    _inherit = "gc.request"

    receiver_id = fields.Reference(
        selection_add=[("gc.builder.world", "gc.builder.world")]
    )
    sender_id = fields.Reference(
        selection_add=[("gc.builder.world", "gc.builder.world")]
    )
    request_type = fields.Selection(
        selection_add=[
            (
                "member_or_team_to_world_invitation",
                "Member or Team to World Invitation",
            )
        ]
    )

    def _check_request_type(self):
        for rec in self:
            if rec.request_type == "member_or_team_to_world_invitation" and (
                rec.receiver_id._name not in ["gc.user", "gc.team"]
                or rec.sender_id._name == "gc.builder.world"
            ):
                raise ValidationError(
                    _(
                        "The receiver needs to be type of 'gc.user'"
                        " or 'gc.team' and the sender type of 'gc.builder.world'!"
                    )
                )
        return super()._check_request_type()

    @api.model
    def get_world_member_or_team_to_world_invitations(self, world_id):
        return [
            {
                "receiver_mc_uuid": x.receiver_id._name == "gc.user"
                and x.receiver_id.mc_uuid,
                "receiver_team_id": x.receiver_id._name == "gc.team"
                and x.receiver_id.id,
                "sender_world_id": x.sender_id.id,
            }
            for x in self.search(
                [
                    ("sender_id", "=", f"gc.builder.world,{world_id}"),
                    ("state", "=", "waiting"),
                    ("request_type", "=", "member_or_team_to_world_invitation"),
                ]
            )
        ]

    @api.model
    def get_user_member_or_team_to_world_invitations(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        return [
            {
                "receiver_mc_uuid": x.receiver_id.mc_uuid,
                "sender_world_id": x.sender_id.id,
            }
            for x in self.search(
                [
                    ("receiver_id", "=", f"gc.user,{user.id}"),
                    ("state", "=", "waiting"),
                    ("request_type", "=", "member_or_team_to_world_invitation"),
                ]
            )
        ]

    @api.model
    def get_team_member_or_team_to_world_invitations(self, team_id):
        return [
            {
                "receiver_team_id": x.receiver_id.id,
                "sender_world_id": x.sender_id.id,
            }
            for x in self.search(
                [
                    ("receiver_id", "=", f"gc.team,{team_id}"),
                    ("state", "=", "waiting"),
                    ("request_type", "=", "member_or_team_to_world_invitation"),
                ]
            )
        ]
