from odoo import fields, models


class GCDiscordEmbedTemplate(models.Model):
    _name = "gc.discord.embed.template"
    _description = "GigaClub Discord Embed Template"

    name = fields.Char()
    title = fields.Char()
    color = fields.Char()
    description = fields.Text()
    image = fields.Char()
    url = fields.Char()
    video = fields.Char()
    embed_field_template_ids = fields.One2many(
        comodel_name="gc.discord.embed.field.template", inverse_name="embed_template_id"
    )
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
