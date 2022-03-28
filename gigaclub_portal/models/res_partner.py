from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    gc_user_id = fields.Many2one(comodel_name="gc.user")
    name = fields.Char(inverse="_inverse_name")

    def _inverse_name(self):
        for rec in self.filtered(lambda x: x.gc_user_id and x.name):
            rec.gc_user_id.name = rec.name

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, rec.name))
        return res
