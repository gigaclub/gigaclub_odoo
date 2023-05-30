from odoo import fields, models


class GCDiscordEmbedFieldTemplate(models.Model):
    _name = "gc.discord.embed.field.template"
    _inherit = "mail.render.mixin"
    _description = "GigaClub Discord Embed Field Template"

    name = fields.Html(render_engine="qweb", sanitize=False)
    value = fields.Html(render_engine="qweb", sanitize=False)
    inline = fields.Boolean(default=True)
    embed_template_id = fields.Many2one(
        comodel_name="gc.discord.embed.template", index=True
    )
    model_id = fields.Many2one(related="embed_template_id.model_id", readonly=True)

    def _compute_render_model(self):
        for rec in self:
            rec.render_model = rec.model_id.model
