from odoo import api, fields, models


class GCTranslation(models.Model):
    _name = "gc.translation"

    name = fields.Char(required=True)
    var_count = fields.Integer()
    translation_entry_ids = fields.Many2many(comodel_name="gc.translation.entry")
    category = fields.Char()

    _sql_constraints = [("name_unique", "unique (name)", "name must be unique!")]

    @api.model
    def get_translation_by_player_uuid(self, name, player_uuid, values=False):
        if not values:
            values = []
        translation = self.search([("name", "=ilike", name)], limit=1)
        if translation:
            translation.var_count = len(values)
        else:
            translation = self.create(
                {
                    "name": name,
                    "var_count": len(values),
                }
            )
        language = (
            self.env["gc.user"].search([("mc_uuid", "=", player_uuid)]).language_id
        )
        entry = (
            self.env["gc.translation.entry"]
            .search([("language_id", "=", language.id)])
            .filtered(lambda x: translation in x.translation_ids)
        )
        if entry:
            return entry[0].content
        return translation.name
