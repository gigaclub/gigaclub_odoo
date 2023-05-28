from odoo import fields, models


class GCDiscordEmbedFooterTemplate(models.Model):
    _name = "gc.discord.embed.footer.template"
    _description = "GigaClub Discord Embed Footer Template"

    name = fields.Char()
    text = fields.Text()
    icon_url = fields.Char()
