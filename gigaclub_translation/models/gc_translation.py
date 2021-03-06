from odoo import api, fields, models


class GCTranslation(models.Model):
    _name = "gc.translation"
    _description = "GigaClub Translation"

    name = fields.Char(required=True)
    values = fields.Text()
    translation_entry_ids = fields.Many2many(comodel_name="gc.translation.entry")
    category = fields.Char()

    # grepper odoo unique sql constraint
    _sql_constraints = [("name_unique", "unique (name)", "name must be unique!")]
    # end grepper

    @api.model
    def get_translation_by_player_uuid(
        self, name, player_uuid, values=False, category=False
    ):
        if not values:
            values = {}
        translation = self.search([("name", "=ilike", name)], limit=1)
        if translation:
            translation.values = values
        else:
            translation = self.create(
                {
                    "name": name,
                    "values": values,
                    "category": category,
                }
            )
        language = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)]).lang
        entry = (
            self.env["gc.translation.entry"]
            .search([("lang", "=", language)])
            .filtered(lambda x: translation in x.translation_ids)
        )
        if entry:
            return entry[0].content
        return translation.name
