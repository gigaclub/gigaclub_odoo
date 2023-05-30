from odoo import fields, models


class GCUser(models.Model):
    _inherit = "gc.user"

    coins = fields.Integer(compute="_compute_coins")
    received_coin_transaction_ids = fields.One2many(
        comodel_name="gc.coins.transaction", inverse_name="receiver_id"
    )
    sent_coin_transaction_ids = fields.One2many(
        comodel_name="gc.coins.transaction", inverse_name="sender_id"
    )

    def _compute_coins(self):
        for rec in self:
            rec.coins = sum(rec.received_coin_transaction_ids.mapped("amount")) - sum(
                rec.sent_coin_transaction_ids.mapped("amount")
            )
