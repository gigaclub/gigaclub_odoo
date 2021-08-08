from odoo import fields, models


class GCTeam(models.Model):
    _name = "gc.team"
    _description = "GigaClub Team"

    name = fields.Char(required=True)
    description = fields.Text()

    user_ids = fields.One2many(
        comodel_name="gc.user", inverse_name="team_user_id", inverse="_inverse_users"
    )
    manager_ids = fields.One2many(
        comodel_name="gc.user", inverse_name="team_manager_id", inverse="_inverse_users"
    )

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]
