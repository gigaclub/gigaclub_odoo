from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCRequest(models.Model):
    _name = "gc.request"
    _description = "GigaClub Request"

    receiver_id = fields.Reference(selection=[("gc.user", "gc.user")])
    sender_id = fields.Reference(selection=[("gc.user", "gc.user")])
    state = fields.Selection(
        selection=[
            ("waiting", "Waiting"),
            ("accepted", "Accepted"),
            ("denied", "Denied"),
        ]
    )

    @api.constrains("receiver_id", "sender_id", "state")
    def _check_duplicate_request(self):
        for rec in self:
            if self.search([("id", "!=", rec.id), ("state", "=", "waiting")]).filtered(
                lambda x: x.receiver_id == rec.receiver_id
                and x.sender_id == rec.sender_id
            ):
                raise ValidationError(_("waiting requests should be unique!"))

    @api.model
    def get_invites(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        return [
            {
                "receiver_type": x.receiver_id._name,
                "receiver_id": x.receiver_id.id,
                "receiver_name": x.receiver_id.name,
                "sender_type": x.sender_id._name,
                "sender_id": x.sender_id.id,
                "sender_name": x.sender_id.name,
            }
            for x in self.search(
                [("receiver_id", "=", user.id), ("state", "=", "waiting")]
            )
        ]
