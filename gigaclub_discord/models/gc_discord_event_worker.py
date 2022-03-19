import requests

from odoo import fields, models


class GCDiscordEventWorker(models.Model):
    _name = "gc.discord.event.worker"
    _description = "GigaClub Discord Event Worker"

    action_worker_id = fields.Many2one(comodel_name="gc.discord.action.worker")
    event_id = fields.Many2one(comodel_name="gc.discord.event")
    current = fields.Boolean(inverse="_inverse_current")
    done = fields.Boolean()

    def start_next_event(self):
        self.ensure_one()
        self.current = False
        self.done = True
        self.search(
            [
                ("event_id", "=", self.event_id.next_event_id.id),
                ("action_worker_id", "=", self.action_worker_id.id),
            ]
        ).current = True

    def _inverse_current(self):
        for rec in self.filtered(lambda x: x.event_id.server_action):
            url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            requests.post(f"{url}/discordbot/event/{rec.id}")
