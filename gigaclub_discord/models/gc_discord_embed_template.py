from odoo import fields, models


class GCDiscordEmbedTemplate(models.Model):
    _name = "gc.discord.embed.template"
    _description = "GigaClub Discord Embed Template"

    color = fields.Char()
    description = fields.Char()
    image = fields.Char()
    url = fields.Char()
    video = fields.Char()
    embed_field_template_ids = fields.One2many(
        comodel_name="gc.discord.embed.field.template", inverse_name="embed_template_id"
    )
    message_template_id = fields.Many2one(
        comodel_name="gc.discord.message.template", index=True
    )
