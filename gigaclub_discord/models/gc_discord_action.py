from odoo import api, fields, models


class GCDiscordAction(models.Model):
    _name = "gc.discord.action"
    _description = "GigaClub Discord Action"

    name = fields.Char(required=True)
    event_ids = fields.One2many(
        comodel_name="gc.discord.event", inverse_name="action_id"
    )
    action_type = fields.Selection(selection=[("user", "User")])
    start_event_id = fields.Many2one(
        comodel_name="gc.discord.event", compute="_compute_start_event", store=True
    )

    @api.depends("event_ids.sequence")
    def _compute_start_event(self):
        for rec in self:
            rec.start_event_id = rec.event_ids.sorted(lambda x: x.sequence)[0]
