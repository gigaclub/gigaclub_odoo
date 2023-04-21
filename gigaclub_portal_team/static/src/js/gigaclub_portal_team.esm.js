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

$("#user-modal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  let data = button.getAttribute("data-bs-dict");
  if (data) {
    data = JSON.parse(data);
    console.log(data);
    // Fill in the user select box with the selected user's name and ID
    $("#select-user option[value='" + data.id + "']").prop("selected", true);
    //    $("#select-user").selectpicker("refresh");

    // Fill in the groups select box with the selected user's groups
    const group_ids = data.groups.map((group) => group.id);
    $("#select-groups").val(group_ids);
    //    $("#select-groups").trigger("change");

    // Fill in the permission checkboxes with the selected user's permissions
    $("#input-user-editteam").prop("checked", data.edit_team);
    $("#input-user-inviteuser").prop("checked", data.invite_user);
    $("#input-user-kickuser").prop("checked", data.kick_user);
    $("#input-user-createworldasteam").prop("checked", data.create_world_as_team);
  }
});
