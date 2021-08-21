from odoo import fields, models


class GCDiscordActionWorker(models.Model):
    _name = "gc.discord.action.worker"
    _description = "GigaClub Discord Action Worker"

    action_id = fields.Many2one(comodel_name="gc.discord.action")
    event_worker_ids = fields.One2many(
        comodel_name="gc.discord.event.worker", inverse_name="action_worker_id"
    )
