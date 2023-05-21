from odoo import fields, models


class GCCoinsTransaction(models.Model):
    _name = "gc.coins.transaction"
    _description = "GigaClub Coins Transaction"

    sender_id = fields.Reference(selection=[("gc.user", "gc.user")])
    receiver_id = fields.Reference(selection=[("gc.user", "gc.user")])
