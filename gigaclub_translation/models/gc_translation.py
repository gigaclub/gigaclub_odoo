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
    def get_translation_by_player_uuid(self, name, player_uuid, category=False):
        translation = self.search([("name", "=ilike", name)], limit=1)
        if not translation:
            translation = self.create(
                {
                    "name": name,
                    "category": category,
                }
            )
        language = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)]).lang
        entry = self.env["gc.translation.entry"].search(
            [("lang", "=", language), ("translation_ids", "in", translation.ids)],
            limit=1,
        )
        if entry:
            return entry.content
        return translation.name
