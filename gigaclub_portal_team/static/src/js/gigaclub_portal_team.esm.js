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

$("#deleteTeamConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const teamId = button.getAttribute("data-bs-team_id");
  window.currentTeamId = teamId;
});

$("#deletePermissionConnectorConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const permissionConnectorId = button.getAttribute("data-bs-permission_connector_id");
  window.currentPermissionConnectorId = permissionConnectorId;
});

$("#deletePermissionGroupConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const permissionGroupId = button.getAttribute("data-bs-permission_group_id");
  window.currentPermissionGroupId = permissionGroupId;
});
