from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    discord_message_id = fields.Many2one(comodel_name="gc.discord.message")
