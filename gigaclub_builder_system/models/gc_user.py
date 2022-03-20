from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCUser(models.Model):
    _inherit = "gc.user"

    world_ids = fields.Many2many(
        comodel_name="gc.builder.world", relation="builder_user_builder_world_rel"
    )
    world_manager_ids = fields.Many2many(
        comodel_name="gc.builder.world",
        relation="builder_manager_user_builder_world_rel",
    )

    @api.constrains("world_ids", "world_manager_ids")
    def _check_team_user_manager_id(self):
        for rec in self:
            if set(rec.world_ids) & set(rec.world_manager_ids):
                raise ValidationError(_("world managers should not be users"))
