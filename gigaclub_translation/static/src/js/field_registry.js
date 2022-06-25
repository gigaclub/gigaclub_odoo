odoo.define("gigaclub_translation.field_registry", function (require) {
  "use strict";

  const MinecraftTellrawField = require("gigaclub_translation.minecraft_tellraw_field");

  const registry = require("web.field_registry_owl");

  registry.add("minecraft_tellraw_field", MinecraftTellrawField.MinecraftTellrawField);
});
