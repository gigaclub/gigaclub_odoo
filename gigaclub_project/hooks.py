from odoo import SUPERUSER_ID, api


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["project.task.stage.personal"].search([]).unlink()
