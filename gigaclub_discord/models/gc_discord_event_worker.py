import requests

from odoo import api, fields, http, models, tools
from odoo.service import security


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
        url = f"http://127.0.0.1:{tools.config['http_port']}"
        session = http.root.session_store.new()
        session.db = self.env.cr.dbname
        uid = self.env.user.id
        env = api.Environment(self.env.cr, self.env.user.id, {})
        session.uid = uid
        session.login = self.env.user.login
        session.session_token = uid and security.compute_session_token(session, env)
        session.context = dict(env["res.users"].context_get() or {})
        session.context["uid"] = uid
        # session._fix_lang(session.context)
        http.root.session_store.save(session)
        opener = requests.Session()
        opener.cookies["session_id"] = session.sid
        self.env.cr.commit()
        for rec in self.filtered(lambda x: x.event_id.server_action and x.current):
            opener.post(f"{url}/discordbot/event/{rec.id}")
