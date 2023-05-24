from odoo import fields, models


class GCDiscordModal(models.Model):
    _name = "gc.discord.modal"
    _description = "GigaClub Discord Modal"

    title = fields.Char()
    custom_id = fields.Char()
    text_input_ids = fields.One2many(
        comodel_name="gc.discord.text.input", inverse_name="modal_id"
    )
