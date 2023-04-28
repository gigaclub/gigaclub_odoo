import random
import string

from odoo import api, fields, models


class GCUser(models.Model):
    _name = "gc.user"
    _description = "GigaClub User"

    name = fields.Char()
    mc_uuid = fields.Char(index=True)
    state = fields.Selection(
        selection=[("online", "Online"), ("offline", "Offline")], default="offline"
    )
    auth_token = fields.Char()

    _sql_constraints = [
        ("mc_uuid_unique", "UNIQUE(mc_uuid)", "MC_UUID must be unique!")
    ]

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f"({rec.name}) - {rec.mc_uuid}"))
        return res

    @api.model
    def generate_auth_token(self, mc_uuid):
        user = self.search([("mc_uuid", "=", mc_uuid)], limit=1)
        if user.auth_token:
            return user.auth_token

        # Define the characters to use in the token
        characters = string.ascii_letters + string.digits

        # Generate a 6-length token
        user.auth_token = "".join(random.choice(characters) for i in range(6))

        user.with_delay(eta=5 * 60).remove_auth_token()

        return user.auth_token

    def remove_auth_token(self):
        self.update({"auth_token": False})
