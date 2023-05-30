from odoo import fields, models


class GCCoinsTransaction(models.Model):
    _name = "gc.coins.transaction"
    _description = "GigaClub Coins Transaction"

    sender_id = fields.Many2one(comodel_name="gc.user", index=True)
    receiver_id = fields.Many2one(comodel_name="gc.user", index=True)
    amount = fields.Integer()
