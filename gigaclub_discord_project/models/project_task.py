from odoo import fields, models
from odoo.tools.mail import html2plaintext


class ProjectTask(models.Model):
    _inherit = "project.task"

    discord_message_id = fields.Many2one(comodel_name="gc.discord.message")

    def add_discord_task_message(self):
        self.ensure_one()
        if self.discord_message_id:
            self.discord_message_id.content = (
                f"New Task {self.name} was created with "
                f"description: {html2plaintext(self.description)}"
            )
            return
        self.discord_message_id = self.env["gc.discord.message"].create(
            {
                "content": f"New Task {self.name} was created "
                f"with description: {html2plaintext(self.description)}",
                "channel_id": self.env.ref(
                    "gigaclub_discord_project.gc_discord_channel_tasks"
                ).id,
            }
        )

    def remove_discord_task_message(self):
        self.ensure_one()
        # TODO add option to delete discord messages
        self.discord_message_id.unlink()
