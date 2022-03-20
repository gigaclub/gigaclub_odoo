from odoo import fields, models


class GCTeam(models.Model):
    _inherit = "gc.team"
    _description = "GigaClub Builder Team"

    world_ids = fields.Many2many(
        comodel_name="gc.builder.world", relation="builder_team_builder_world_rel"
    )
    world_manager_ids = fields.Many2many(
        comodel_name="gc.builder.world",
        relation="builder_manager_team_builder_world_rel",
    )

    def return_team(self, team):
        res = super().return_team(team)
        res.update(
            {
                "world_ids": [{"id": w.id} for w in team.world_ids],
                "world_manager_ids": [{"id": w.id} for w in team.world_manager_ids],
            }
        )
        return res
