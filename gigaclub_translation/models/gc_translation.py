from odoo import api, fields, models


class GCTranslation(models.Model):
    _name = "gc.translation"

    name = fields.Char(required=True)
    var_count = fields.Integer()
    translation_entry_ids = fields.Many2many(comodel_name="gc.translation.entry")

    _sql_constraints = [("name_unique", "unique (name)", "name must be unique!")]

    @api.model
    def get_translation_by_player_uuid(self, name, player_uuid, values=False):
        if not values:
            values = []
        translation_id = self.search([("name", "=ilike", name)], limit=1)
        if len(translation_id) == 1:
            translation_id.var_count = len(values)
        else:
            translation_id = self.create(
                {
                    "name": name,
                    "var_count": len(values),
                }
            )
        language_id = (
            self.env["gc.user"].search([("mc_uuid", "=", player_uuid)]).language_id
        )
        entry_id = (
            self.env["gc.translation.entry"]
            .search([("language_id", "=", language_id.id)])
            .filtered(lambda x: translation_id in x.translation_ids)
        )
        if len(entry_id) > 0:
            return entry_id[0].content
        return translation_id.name
