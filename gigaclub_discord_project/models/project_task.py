from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    discord_message_id = fields.Many2one(comodel_name="gc.discord.message")

    def add_discord_task_message(self):
        self.ensure_one()
        if self.discord_message_id:
            # self.discord_message_id.content = (
            #     f"New Task {self.name} was created with "
            #     f"description: {html2plaintext(self.description or '')}"
            # )
            return
        # self.discord_message_id = self.env["gc.discord.message"].create(
        #     {
        #         "content": f"New Task {self.name} was created "
        #         f"with description: {html2plaintext(self.description or '')}",
        #         "channel_id": self.env.ref(
        #             "gigaclub_discord_project.gc_discord_channel_tasks"
        #         ).id,
        #     }
        # )
        message_template = self.env.ref(
            "gigaclub_discord_project.gc_discord_message_template_task"
        )
        self.discord_message_id = message_template.create_message(
            self.env.ref("gigaclub_discord_project.gc_discord_channel_tasks"), self.id
        )

    def remove_discord_task_message(self):
        self.ensure_one()
        # TODO add option to delete discord messages
        self.discord_message_id.unlink()
