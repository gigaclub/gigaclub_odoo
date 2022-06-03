from odoo import api, fields, models


class GCPermissionGroup(models.Model):
    _name = "gc.permission.group"
    _description = "GigaClub Permission Group"

    name = fields.Char()
    description = fields.Text()
    permission_profile_ids = fields.Many2many(comodel_name="gc.permission.profile")
    global_group = fields.Boolean()

    @api.model
    def get_all_groups(self):
        return [
            {"id": x.id, "name": x.name, "description": x.description}
            for x in self.search([("global_group", "=", True)])
        ]
