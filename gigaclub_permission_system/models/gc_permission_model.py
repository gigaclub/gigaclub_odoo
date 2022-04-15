from odoo import fields, models


class GCPermissionModel(models.Model):
    _name = "gc.permission.model"
    _description = "GigaClub Permission Model"

    name = fields.Char(reference="model_id.name", required=True)
    model_id = fields.Many2one(comodel_name="ir.model", required=True)
    permission_model_entry_ids = fields.One2many(
        comodel_name="gc.permission.model.entry", inverse_name="permission_model_id"
    )
