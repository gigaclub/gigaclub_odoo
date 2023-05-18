from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCDiscordCategory(models.Model):
    _name = "gc.discord.category"
    _description = "GigaClub Discord Category"

    name = fields.Char(translate=True, required=True)
    discord_channel_uuid = fields.Char(readonly=True)
    channel_ids = fields.One2many(
        comodel_name="gc.discord.channel", inverse_name="category_id"
    )
    overwrite_permission_profile_ids = fields.One2many(
        comodel_name="gc.discord.permission.profile.overwrite",
        inverse_name="category_id",
    )

    @api.constrains("channel_ids")
    def _check_channel_ids(self):
        for rec in self:
            if len(rec.channel_ids) > 50:
                raise ValidationError(
                    _("A category can just have a maximum of 50 channels!")
                )
