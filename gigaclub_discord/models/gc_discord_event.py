from odoo import api, fields, models


class GCDiscordEvent(models.Model):
    _name = "gc.discord.event"
    _description = "GigaClub Discord Event"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    action_id = fields.Many2one(comodel_name="gc.discord.action")
    event_type = fields.Selection(
        selection=[
            ("guild_join", "On Guild Join"),
            ("send_private_message", "Send private Message"),
            ("get_private_message", "Get Private Message"),
            ("set_role", "Set Role"),
        ]
    )
    user_action = fields.Boolean(compute="_compute_action", store=True)
    server_action = fields.Boolean(compute="_compute_action", store=True)
    message_content = fields.Text()
    role_id = fields.Many2one(comodel_name="gc.discord.role")

    @api.depends("event_type")
    def _compute_action(self):
        for rec in self:
            rec.user_action = rec.event_type in ["guild_join", "get_private_message"]
            rec.server_action = rec.event_type in ["send_private_message", "set_role"]
