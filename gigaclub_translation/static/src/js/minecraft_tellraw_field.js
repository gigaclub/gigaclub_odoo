odoo.define("gigaclub_translation.minecraft_tellraw_field", function (require) {
  "use strict";

  const minecraftTellrawFieldModule = require("minecraft_tellraw_field.minecraft_tellraw_field");
  const OwlDialog = require("web.OwlDialog");
  const minecraftTellrawField = minecraftTellrawFieldModule.MinecraftTellrawField;
  const minecraftTellrawDialog = minecraftTellrawFieldModule.MinecraftTellrawDialog;
  const {Component} = owl;
  const {useState} = owl.hooks;

  class MinecraftTellrawListWidgetDialog extends Component {
    constructor(...args) {
      super(...args);
      this.state = useState({
        values: ["", {text: "placeholder", listitem: true}],
        text: "test",
        widgets: {params: [], list: []},
      });
      this.mode = "edit";
      this.state.widgets = this.__owl__.parent.state.widgets;
    }
    patched() {
      this._reInitDropdown();
    }
    _reInitDropdown() {
      //grepper jquery init dropdown
      $(document).ready(function () {
        $(".dropdown-toggle").dropdown();
      });
      //end grepper
    }
  }

  Object.assign(MinecraftTellrawListWidgetDialog, {
    components: {
      Dialog: OwlDialog,
    },
    template: "MinecraftTellrawListWidgetDialog",
  });

  class MinecraftTellrawDialog extends minecraftTellrawDialog {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {widgets: {params: [], list: []}})
      );
      this.state.widgets = this.__owl__.parent.state.widgets;
    }
  }

  class MinecraftTellrawField extends minecraftTellrawField {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {
          widgets: {params: [], list: []},
          minecraftTellrawListWidgetDialog: false,
        })
      );
    }
    willStart() {
      this.state.widgets = this.props.record.data.widgets;
    }
    openList() {
      this.state.minecraftTellrawListWidgetDialog = true;
    }
    onListWidgetDialogClosed() {
      this.state.minecraftTellrawListWidgetDialog = false;
    }
  }

  Object.assign(MinecraftTellrawField, {
    components: {
      MinecraftTellrawDialog,
      MinecraftTellrawListWidgetDialog,
    },
    template: "FieldMinecraftTellrawInheritGigaClubTranslation",
  });

  return {
    MinecraftTellrawField: MinecraftTellrawField,
    MinecraftTellrawDialog: MinecraftTellrawDialog,
  };
});
