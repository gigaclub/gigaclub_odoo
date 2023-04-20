/** @odoo-module */

import publicWidget from "web.public.widget";

publicWidget.registry.PortalHomeCounters.include({
  /**
   * @override
   */
  _getCountersAlwaysDisplayed() {
    return this._super(...arguments).concat(["team_count"]);
  },
});

$(".js-select-user-single").select2({
  allowClear: true,
  minimumInputLength: 0,
  dropdownCssClass: "oe_import_selector",
});
$(".js-select-groups-multiple").select2({});
