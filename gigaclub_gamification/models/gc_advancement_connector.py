from odoo import fields, models


class GCAdvancementConnector(models.Model):
    _name = "gc.advancement.connector"
    _description = "GigaClub Advancement Connector"

    user_id = fields.Many2one(comodel_name="gc.user")
    advancement_id = fields.Many2one(comodel_name="gc.advancement")
