from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GCLanguage(models.Model):
    _name = "gc.language"

    name = fields.Char(required=True)
    entry_ids = fields.One2many(
        comodel_name="gc.translation.entry", inverse_name="translation_id"
    )
    default = fields.Boolean()

    _sql_constraints = [("name_unique", "unique (name)", "name must be unique!")]

    @api.constrains("default")
    def _check_default(self):
        for rec in self:
            if rec.default and self.search_count([("default", "=", True)]) > 1:
                raise ValidationError(_("default must be unique!"))
