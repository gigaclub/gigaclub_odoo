from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCUser(models.Model):
    _inherit = "gc.user"

    team_manager_id = fields.Many2one(comodel_name="gc.team")
    team_user_id = fields.Many2one(comodel_name="gc.team")

    @api.constrains("team_user_id", "team_manager_id")
    def _check_team_user_manager_id(self):
        for rec in self:
            if rec.team_user_id and rec.team_manager_id:
                raise ValidationError(_("managers should not be users"))
