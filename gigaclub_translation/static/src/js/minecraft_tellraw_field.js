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
        text: "",
        widgets: {params: [], list: []},
        minecraftTellrawTextDialog: false,
        editValue: {},
      });
      this.mode = "edit";
      // Grepper owl get parent state
      this.state.widgets = this.__owl__.parent.state.widgets;
      // End grepper
    }
    patched() {
      this._reInitDropdown();
      this._reInitSortable();
      this._generatePreviewText();
    }
    openText() {
      this.state.minecraftTellrawTextDialog = true;
    }
    onClickSave() {
      if (!this.__owl__.parent.state.fromEdit) {
        Array.prototype.push.apply(this.__owl__.parent.state.values, this.state.values);
      }
      this.__owl__.parent.state.fromEdit = false;
      this.__owl__.parent.state.minecraftTellrawListWidgetDialog = false;
    }
    onClickCancel() {
      this.__owl__.parent.state.minecraftTellrawListWidgetDialog = false;
    }
    _generatePreviewText() {
      const value = this.state.value;
      if (value) {
        if (value.hasOwnProperty("text")) {
          const valueSpan = $("<span />");
          valueSpan.text(value.text);
          if (value.hasOwnProperty("color")) {
            valueSpan.css("color", value.color);
          }
          if (value.hasOwnProperty("bold")) {
            valueSpan.css("font-weight", value.bold ? "bold" : "normal");
          }
          if (value.hasOwnProperty("italic")) {
            valueSpan.css("font-style", value.italic ? "italic" : "normal");
          }
          if (value.hasOwnProperty("underlined")) {
            valueSpan.css("text-decoration", value.underlined ? "underline" : "none");
          }
          if (value.hasOwnProperty("strikethrough")) {
            valueSpan.css(
              "text-decoration",
              value.strikethrough ? "line-through" : valueSpan.css("text-decoration")
            );
          }
          if (
            value.hasOwnProperty("underlined") &&
            value.hasOwnProperty("strikethrough") &&
            value.underlined &&
            value.strikethrough
          ) {
            valueSpan.css("text-decoration", "underline line-through");
          }
          this.state.previewText = valueSpan[0].outerHTML;
        }
      }
    }
    _reInitDropdown() {
      // Grepper jquery init dropdown
      $(document).ready(function () {
        $(".dropdown-toggle").dropdown();
      });
      // End grepper
    }
    _reInitSortable() {
      $("table tbody").sortable({
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
