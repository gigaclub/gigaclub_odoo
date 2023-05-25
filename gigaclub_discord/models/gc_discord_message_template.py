from odoo import fields, models


class GCDiscordMessageTemplate(models.Model):
    _name = "gc.discord.message.template"
    _description = "GigaClub Discord Message Template"

    name = fields.Char()
    embed_template_ids = fields.One2many(
        comodel_name="gc.discord.embed.template", inverse_name="message_template_id"
    )
    content_template = fields.Html(render_engine="qweb", translate=True)
    view_ids = fields.Many2many(comodel_name="gc.discord.view")

    def create_message(self):
        self.ensure_one()
