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
        minecraftTellrawTextDialog: false,
      });
      this.mode = "edit";
      // Grepper owl get parent state
      this.state.widgets = this.__owl__.parent.state.widgets;
      // End grepper
    }
    patched() {
      this._reInitDropdown();
    }
    openText() {
      this.state.minecraftTellrawTextDialog = true;
    }
    onClickSave() {
      if (this.state.hoverEvent === "show_text") {
        this.state.value.hoverEvent = {
          action: this.state.hoverEvent,
          value: this.state.values,
        };
      }
      if (!this.__owl__.parent.state.fromEdit) {
        this.__owl__.parent.state.values.push(this.state.value);
      }
      this.__owl__.parent.state.fromEdit = false;
      this.__owl__.parent.state.minecraftTellrawTextDialog = false;
    }
    onClickCancel() {
      this.__owl__.parent.state.minecraftTellrawTextDialog = false;
    }
    _reInitDropdown() {
      // Grepper jquery init dropdown
      $(document).ready(function () {
        $(".dropdown-toggle").dropdown();
      });
      // End grepper
    }
  }

  Object.assign(MinecraftTellrawListWidgetDialog, {
    components: {
      Dialog: OwlDialog,
      MinecraftTellrawDialog: minecraftTellrawDialog,
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
      this.showWidgets = true;
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
