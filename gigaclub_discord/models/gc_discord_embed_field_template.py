from odoo import fields, models


class GCDiscordEmbedFieldTemplate(models.Model):
    _name = "gc.discord.embed.field.template"
    _description = "GigaClub Discord Embed Field Template"

    name = fields.Char()
    value = fields.Char()
    inline = fields.Boolean(default=True)
    embed_template_id = fields.Many2one(
        comodel_name="gc.discord.embed.template", index=True
    )
