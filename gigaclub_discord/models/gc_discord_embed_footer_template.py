from odoo import fields, models


class GCDiscordEmbedFooterTemplate(models.Model):
    _name = "gc.discord.embed.footer.template"
    _inherit = "mail.render.mixin"
    _description = "GigaClub Discord Embed Footer Template"

    name = fields.Char()
    text = fields.Html(render_engine="qweb", sanitize=False)
    icon_url = fields.Char()
    model_id = fields.Many2one(comodel_name="ir.model")

    def _compute_render_model(self):
        for rec in self:
            rec.render_model = rec.model_id.model
