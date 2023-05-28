from odoo import fields, models


class GCDiscordEmbedFooterTemplate(models.Model):
    _name = "gc.discord.embed.footer.template"
    _inherit = "mail.render.mixin"
    _description = "GigaClub Discord Embed Footer Template"

    name = fields.Char()
    text = fields.Html(render_engine="qweb")
    icon_url = fields.Char()
