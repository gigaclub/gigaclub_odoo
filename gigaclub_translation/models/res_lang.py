from odoo import api, models, tools


class ResLang(models.Model):
    _inherit = "res.lang"

    @api.model
    def install_lang(self):
        res = super().install_lang()
        lang_code = (tools.config.get("load_language") or "en_US").split(",")[0]
        IrDefault = self.env["ir.default"]
        default_user_value = IrDefault.get("gc.user", "lang")
        if default_user_value is None:
            IrDefault.set("gc.user", "lang", lang_code)
        default_translation_entry_value = IrDefault.get("gc.translation.entry", "lang")
        if default_translation_entry_value is None:
            IrDefault.set("gc.translation.entry", "lang", lang_code)
        return res
