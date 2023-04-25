/** @odoo-module */

import publicWidget from "web.public.widget";

publicWidget.registry.PortalHomeCounters.include({
  /**
   * @override
   */
  _getCountersAlwaysDisplayed() {
    return this._super(...arguments).concat(["world_count"]);
  },
});

$(".js-select-worldtype-single").select2({});
$(".js-select-task-single").select2({});

$("#deleteWorldConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const worldId = button.getAttribute("data-bs-world_id");
  window.currentWorldId = worldId;
});

$("#deleteUserPermissionConnectorConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const userPermissionConnectorId = button.getAttribute(
    "data-bs-permission_connector_id"
  );
  window.currentUserPermissionConnectorId = userPermissionConnectorId;
});

$("#deleteTeamPermissionConnectorConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const teamPermissionConnectorId = button.getAttribute(
    "data-bs-permission_connector_id"
  );
  window.currentTeamPermissionConnectorId = teamPermissionConnectorId;
});

$("#world-user-modal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  let data = button.getAttribute("data-bs-dict");

  let users = button.getAttribute("data-bs-users");
  users = JSON.parse(users);
  const $selectUser = $("#select-user");
  $selectUser.empty();
  $selectUser.append($("<option>").val("").text("")); // Add empty option
  for (const user of users) {
    const $option = $("<option>").val(user.id).text(user.name);
    $selectUser.append($option);
  }
  $selectUser.val(null).trigger("change");

  $("#input-user-inviteuser").prop("checked", false);
  $("#input-user-inviteteam").prop("checked", false);
  $("#input-user-removeuser").prop("checked", false);
  $("#input-user-removeteam").prop("checked", false);
  $("#input-user-saveworld").prop("checked", false);
  $("#input-user-editworldtype").prop("checked", false);

  if (data) {
    data = JSON.parse(data);

    const $option = $("<option>").val(data.id).text(data.name);
    $selectUser.append($option);
    $selectUser.val(data.id).trigger("change");

    // Fill in the permission checkboxes with the selected user's permissions
    $("#input-user-inviteuser").prop("checked", data.invite_user);
    $("#input-user-inviteteam").prop("checked", data.invite_team);
    $("#input-user-removeuser").prop("checked", data.remove_user);
    $("#input-user-removeteam").prop("checked", data.remove_team);
    $("#input-user-saveworld").prop("checked", data.save_world);
    $("#input-user-editworldtype").prop("checked", data.edit_world_type);
  }
});

$("#world-team-modal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  let data = button.getAttribute("data-bs-dict");

  let teams = button.getAttribute("data-bs-teams");
  teams = JSON.parse(teams);
  const $selectTeam = $("#select-team");
  $selectTeam.empty();
  $selectTeam.append($("<option>").val("").text("")); // Add empty option
  for (const team of teams) {
    const $option = $("<option>").val(team.id).text(team.name);
    $selectTeam.append($option);
  }
  $selectTeam.val(null).trigger("change");

  $("#input-team-inviteuser").prop("checked", false);
  $("#input-team-inviteteam").prop("checked", false);
  $("#input-team-removeuser").prop("checked", false);
  $("#input-team-removeteam").prop("checked", false);
  $("#input-team-saveworld").prop("checked", false);
  $("#input-team-editworldtype").prop("checked", false);

  if (data) {
    data = JSON.parse(data);

    const $option = $("<option>").val(data.id).text(data.name);
    $selectTeam.append($option);
    $selectTeam.val(data.id).trigger("change");

    // Fill in the permission checkboxes with the selected user's permissions
    $("#input-team-inviteuser").prop("checked", data.invite_user);
    $("#input-team-inviteteam").prop("checked", data.invite_team);
    $("#input-team-removeuser").prop("checked", data.remove_user);
    $("#input-team-removeteam").prop("checked", data.remove_team);
    $("#input-team-saveworld").prop("checked", data.save_world);
    $("#input-team-editworldtype").prop("checked", data.edit_world_type);
  }
});
