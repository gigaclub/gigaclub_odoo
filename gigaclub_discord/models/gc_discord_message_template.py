from odoo import fields, models


class GCDiscordMessageTemplate(models.Model):
    _name = "gc.discord.message.template"
    _description = "GigaClub Discord Message Template"

    name = fields.Char()
    embed_template_ids = fields.One2many(
        comodel_name="gc.discord.embed.template", inverse_name="message_template_id"
    )
    view_id = fields.Many2one(comodel_name="gc.discord.view")
    model_id = fields.Many2one(comodel_name="ir.model")

    def create_message(self, channel):
        self.ensure_one()
        content = {
            "embeds": [
                {
                    "title": embed.title,
                    "color": embed.color,
                    "description": embed.description,
                    "image": embed.image,
                    "url": embed.url,
                    "video": embed.video,
                    "type": embed.type,
                    "fields": [
                        {
                            "name": field.name,
                            "value": field.value,
                            "inline": field.inline,
                        }
                        for field in embed.embed_field_template_ids
                    ],
                    "footer": {
                        "text": embed.embed_footer_id.text,
                        "icon_url": embed.embed_footer_id.icon_url,
                    },
                }
                for embed in self.embed_template_ids
            ],
            "view": [
                {
                    "buttons": [
                        {"name": button.name, "custom_id": button.custom_id}
                        for button in self.view_id.button_ids
                    ]
                },
                {
                    "selects": [
                        {
                            "name": select.name,
                            "custom_id": select.custom_id,
                            "select_items": [
                                {"name": item.name} for item in select.select_item_ids
                            ],
                        }
                        for select in self.view_id.select_ids
                    ]
                },
            ],
        }
        return self.env["gc.discord.message"].create(
            [
                {
                    "content": content,
                    "message_template_id": self.id,
                    "channel_id": channel.id,
                }
            ]
        )
