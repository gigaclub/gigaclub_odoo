from odoo import fields, models


class GCDiscordMessage(models.Model):
    _name = "gc.discord.message"
    _description = "GigaClub Discord Message"

    content = fields.Text()
    message_id = fields.Char()
    channel_id = fields.Many2one(comodel_name="gc.discord.channel")
    sent = fields.Boolean()
    message_template_id = fields.Many2one(comodel_name="gc.discord.message.template")
