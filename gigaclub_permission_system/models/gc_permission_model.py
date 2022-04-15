from odoo import fields, models


class GCPermissionModel(models.Model):
    _name = "gc.permission.model"
    _description = "GigaClub Permission Model"

    name = fields.Char(related="model_id.name", readonly=True)
    model_id = fields.Many2one(comodel_name="ir.model")
    permission_model_entry_ids = fields.One2many(
        comodel_name="gc.permission.model.entry", inverse_name="permission_model_id"
    )
