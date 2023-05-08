from odoo import fields, models


class GCException(models.Model):
    _name = "gc.exception"
    _description = "GigaClub Exception"

    name = fields.Char(readonly=True)
    traceback = fields.Text(readonly=True)
