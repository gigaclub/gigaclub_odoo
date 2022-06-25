odoo.define("gigaclub_translation.minecraft_tellraw_field", function (require) {
  "use strict";

  const minecraftTellrawFieldModule = require("minecraft_tellraw_field.minecraft_tellraw_field");
  const minecraftTellrawField = minecraftTellrawFieldModule.MinecraftTellrawField;
  const minecraftTellrawDialog = minecraftTellrawFieldModule.MinecraftTellrawDialog;
  const {useState} = owl.hooks;

  class MinecraftTellrawDialog extends minecraftTellrawDialog {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {widgets: {params: [], list: []}})
      );
    }
    willStart() {
      this.state.widgets = this.__owl__.parent.state.widgets;
    }
  }

  class MinecraftTellrawField extends minecraftTellrawField {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {widgets: {params: [], list: []}})
      );
    }
    willStart() {
      this.state.widgets = this.props.record.data.widgets;
    }
  }

  Object.assign(MinecraftTellrawField, {
    components: {
      MinecraftTellrawDialog,
    },
  });

  return {
    MinecraftTellrawField: MinecraftTellrawField,
    MinecraftTellrawDialog: MinecraftTellrawDialog,
  };
});
