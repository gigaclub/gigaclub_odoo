from odoo import fields, models


class GCDiscordEmbedTemplate(models.Model):
    _name = "gc.discord.embed.template"
    _inherit = "mail.render.mixin"
    _description = "GigaClub Discord Embed Template"

    name = fields.Char()
    title = fields.Html(render_engine="qweb")
    color = fields.Char()
    description = fields.Html(render_engine="qweb")
    image = fields.Char()
    url = fields.Char()
    video = fields.Char()
    embed_field_template_ids = fields.One2many(
        comodel_name="gc.discord.embed.field.template", inverse_name="embed_template_id"
    )
    model_id = fields.Many2one(related="message_template_id.model_id", readonly=True)
    message_template_id = fields.Many2one(
        comodel_name="gc.discord.message.template", index=True
    )
    type = fields.Selection(
        selection=[
            ("rich", "Rich"),
            ("image", "Image"),
            ("video", "Video"),
            ("gifv", "Gifv"),
            ("article", "Article"),
            ("link", "Link"),
        ],
        default="rich",
    )
    embed_footer_id = fields.Many2one(comodel_name="gc.discord.embed.footer.template")
