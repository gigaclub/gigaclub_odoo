from odoo import api, fields, models


class GCWarningType(models.Model):
    _name = "gc.warning.type"
    _description = "GigaClub Warning Type"

    name = fields.Char()
    description = fields.Text()
    ban_time = fields.Float()
    expiration_time = fields.Float()
    points = fields.Integer()

    @api.model
    def get_warning_types(self) -> list:
        return [
            {
                "name": x.name,
                "description": x.descriotion,
                "ban_time": x.ban_time,
                "expiration_time": x.expiration_time,
                "points": x.points,
            }
            for x in self.search([])
        ]
