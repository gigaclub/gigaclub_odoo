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
        values: ["", {text: this.props.widget, listitem: true}],
        text: "",
        widgets: {params: [], list: []},
        minecraftTellrawTextDialog: false,
        editValue: {},
        widget: "",
        fromEdit: false,
        index: 0,
        previewText: "",
      });
      this.mode = "edit";
      // Grepper owl get parent state
      this.state.widgets = this.__owl__.parent.state.widgets;
      // End grepper
      this.state.widget = this.props.widget;
      this.state.text = this.state.widget;
    }
    mounted() {
      if (Object.keys(this.props.editValue).length) {
        this._setEditValue(this.props.editValue);
      }
    }
    patched() {
      this._reInitDropdown();
      this._reInitSortable();
    }
    openText() {
      this.state.minecraftTellrawTextDialog = true;
    }
    onClickSave() {
      if (!this.__owl__.parent.state.fromEdit) {
        this.__owl__.parent.state.values.push({
          text: this.state.text,
          widget: this.state.widget,
          type: "list",
          values: this.state.values,
        });
      }
      this.__owl__.parent.state.fromEdit = false;
      this.__owl__.parent.state.minecraftTellrawListWidgetDialog = false;
    }
    onClickCancel() {
      this.__owl__.parent.state.minecraftTellrawListWidgetDialog = false;
    }
    onClickEditText(index) {
      this.state.fromEdit = true;
      this.state.editValue = this.state.values[index];
      this.state.index = index;
      this.state.minecraftTellrawTextDialog = true;
    }
    onDialogClosed() {
      this.state.minecraftTellrawTextDialog = false;
    }
    _reInitDropdown() {
      // Grepper jquery init dropdown
      $(document).ready(function () {
        $(".dropdown-toggle").dropdown();
      });
      // End grepper
    }
    _reInitSortable() {
      $("table tbody.dropdown-values").sortable({
        handle: "span.o_row_handle",
        cancel: "",
        start: (e, ui) => {
          $(this).attr("data-previndex", ui.item.index());
        },
        update: (e, ui) => {
          const oldIndex = $(this).attr("data-previndex");
          const newIndex = ui.item.index();
          $(this).removeAttr("data-previndex");
          this._updateIndex(oldIndex + 1, newIndex + 1);
        },
      });
    }
    _setEditValue(value) {
      this.state.values = value.values;
      this.__owl__.parent.state.editValue = {};
    }
    _updateIndex(oldIndex, newIndex) {
      const values = this.state.values;
      const value = values[oldIndex];
      values.splice(oldIndex, 1);
      values.splice(newIndex, 0, value);
      this.state.values = values;
      // Close dialog because the index changed and the old index is no longer valid
      // should be solved by a better solution
      this.onClickSave();
    }
  }

  class MinecraftTellrawDialog extends minecraftTellrawDialog {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {widgets: {params: [], list: []}})
      );
      this.state.widgets = this.__owl__.parent.state.widgets;
    }
  }

  Object.assign(MinecraftTellrawListWidgetDialog, {
    components: {
      Dialog: OwlDialog,
      MinecraftTellrawDialog: MinecraftTellrawDialog,
    },
    template: "MinecraftTellrawListWidgetDialog",
  });

  class MinecraftTellrawField extends minecraftTellrawField {
    constructor(...args) {
      super(...args);
      this.state = useState(
        Object.assign({}, this.state, {
          widgets: {params: [], list: []},
          minecraftTellrawListWidgetDialog: false,
          widget: "",
        })
      );
      this.showWidgets = true;
    }
    willStart() {
      this.state.widgets = this.props.record.data.widgets;
    }
    openList(event) {
      this.state.widget = event.target.name;
      this.state.minecraftTellrawListWidgetDialog = true;
    }
    onListWidgetDialogClosed() {
      this.state.minecraftTellrawListWidgetDialog = false;
    }
    onClickEditText(index) {
      this.state.fromEdit = true;
      this.state.editValue = this.state.values[index];
      if (this.state.editValue.type && this.state.editValue.type === "list") {
        this.state.minecraftTellrawListWidgetDialog = true;
      } else {
        this.state.minecraftTellrawTextDialog = true;
      }
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
