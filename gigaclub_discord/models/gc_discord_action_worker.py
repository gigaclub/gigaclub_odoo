from odoo import api, fields, models


class GCDiscordActionWorker(models.Model):
    _name = "gc.discord.action.worker"
    _description = "GigaClub Discord Action Worker"

    action_id = fields.Many2one(comodel_name="gc.discord.action")
    event_worker_ids = fields.One2many(
        comodel_name="gc.discord.event.worker", inverse_name="action_worker_id"
    )
    gc_user_id = fields.Many2one(comodel_name="gc.user")
    current_event_worker_id = fields.Many2one(
        comodel_name="gc.discord.event.worker",
        compute="_compute_current_event",
        store=True,
    )

    @api.depends("event_worker_ids.current")
    def _compute_current_event(self):
        for rec in self:
            event_workers = self.event_worker_ids.filtered(
                lambda x: x.current and not x.done
            )
            rec.current_event_worker_id = event_workers and event_workers[0]

    @api.model
    def create_worker(self, action, user):
        GCDiscordEventWorker = self.env["gc.discord.event.worker"]
        action_worker = self.search(
            [("action_id", "=", action.id), ("gc_user_id", "=", user.id)], limit=1
        )
        if action_worker:
            return action_worker
        event_worker_ids = GCDiscordEventWorker
        for event in action.event_ids:
            event_worker_ids |= GCDiscordEventWorker.create(
                {
                    "event_id": event.id,
                }
            )
        start_event = action.start_event_id
        start_event_worker = GCDiscordEventWorker.search(
            [("event_id", "=", start_event.id)]
        )
        start_event_worker.current = True
        res = self.create(
            {
                "action_id": action.id,
                "event_worker_ids": [[6, 0, event_worker_ids.ids]],
                "gc_user_id": user.id,
            }
        )
        return res
