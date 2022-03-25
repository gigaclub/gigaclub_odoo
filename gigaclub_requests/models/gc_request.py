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
