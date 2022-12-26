odoo.define("gigaclub_portal_team.gigaclub_portal_team", () => {
  "use strict";

  $(".js-select-user-single").select2({
    allowClear: true,
    minimumInputLength: 0,
    dropdownCssClass: "oe_import_selector",
  });
  $(".js-select-groups-multiple").select2({});
});
