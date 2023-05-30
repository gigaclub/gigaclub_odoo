import requests

from odoo import api, fields, http, models, registry, tools
from odoo.service import security


class GCDiscordEventWorker(models.Model):
    _name = "gc.discord.event.worker"
    _description = "GigaClub Discord Event Worker"

    action_worker_id = fields.Many2one(comodel_name="gc.discord.action.worker")
    event_id = fields.Many2one(comodel_name="gc.discord.event", index=True)
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
        self.with_delay().call_events()

    def call_events(self):
        with registry(self.env.cr.dbname).cursor() as new_cr:
            new_env = api.Environment(new_cr, self.env.uid, self.env.context)
            url = f"http://127.0.0.1:{tools.config['http_port']}"
            session = http.root.session_store.new()
            session.db = new_env.cr.dbname
            uid = new_env.user.id
            session.uid = uid
            session.login = new_env.user.login
            session.session_token = uid and security.compute_session_token(
                session, new_env
            )
            session.context = dict(new_env["res.users"].context_get() or {})
            session.context["uid"] = uid
            http.root.session_store.save(session)
            opener = requests.Session()
            opener.cookies["session_id"] = session.sid
            for rec in self.filtered(lambda x: x.event_id.server_action and x.current):
                opener.post(f"{url}/discordbot/event/{rec.id}")
