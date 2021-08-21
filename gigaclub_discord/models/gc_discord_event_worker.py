from odoo import fields, models


class GCDiscordEventWorker(models.Model):
    _name = "gc.discord.event.worker"
    _description = "GigaClub Discord Event Worker"

    action_worker_id = fields.Many2one(comodel_name="gc.discord.action.worker")
    event_id = fields.Many2one(comodel_name="gc.discord.event")
    current = fields.Boolean(inverse="_inverse_current")
    done = fields.Boolean()

    gc_user_id = fields.Many2one(comodel_name="gc.user")

    def _inverse_current(self):
        for rec in self:
            return {
                "name": "event",
                "res_model": "ir.actions.act_url",
                "type": "ir.actions.act_url",
                "target": "_blank",
                "url": f"/discordbot/event/{rec.id}",
            }
