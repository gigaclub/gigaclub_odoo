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

$(".js-select-user-single").select2({});
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

  let groups = button.getAttribute("data-bs-groups");
  groups = JSON.parse(groups);
  const $selectGroup = $("#select-groups");
  $selectGroup.empty();
  for (const group of groups) {
    const $option = $("<option>").val(group.id).text(group.name);
    $selectGroup.append($option);
  }
  $selectGroup.val([]).trigger("change");

  $("#input-user-editteam").prop("checked", false);
  $("#input-user-inviteuser").prop("checked", false);
  $("#input-user-kickuser").prop("checked", false);
  $("#input-user-createworldasteam").prop("checked", false);

  if (data) {
    data = JSON.parse(data);

    const $option = $("<option>").val(data.id).text(data.name);
    $selectUser.append($option);
    $selectUser.val(data.id).trigger("change");

    for (const group of data.groups) {
      const $option = $("<option>").val(group.id).text(group.name);
      $selectGroup.append($option);
      $selectGroup.val(group.id).trigger("change");
    }

    // Fill in the permission checkboxes with the selected user's permissions
    $("#input-user-editteam").prop("checked", data.edit_team);
    $("#input-user-inviteuser").prop("checked", data.invite_user);
    $("#input-user-kickuser").prop("checked", data.kick_user);
    $("#input-user-createworldasteam").prop("checked", data.create_world_as_team);
  }
});

$("#group-modal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  let data = button.getAttribute("data-bs-dict");

  $("#input-id").val("");
  $("#input-name").val("");
  $("#textarea-description").val("");

  $("#input-group-editteam").prop("checked", false);
  $("#input-group-inviteuser").prop("checked", false);
  $("#input-group-kickuser").prop("checked", false);
  $("#input-group-createworldasteam").prop("checked", false);

  let groups = button.getAttribute("data-bs-groups");
  groups = JSON.parse(groups);
  const $selectParentGroup = $("#select-parentgroup");
  $selectParentGroup.empty();
  $selectParentGroup.append($("<option>").val("").text("")); // Add empty option
  for (const group of groups) {
    const $option = $("<option>").val(group.id).text(group.name);
    $selectParentGroup.append($option);
  }
  $selectParentGroup.val(null).trigger("change");

  const $selectChildGroups = $("#select-childgroups");
  $selectChildGroups.empty();
  for (const group of groups) {
    const $option = $("<option>").val(group.id).text(group.name);
    $selectChildGroups.append($option);
  }
  $selectChildGroups.val([]).trigger("change");
  if (data) {
    data = JSON.parse(data);

    $("#input-id").val(data.id);
    $("#input-name").val(data.name);
    if (data.description) {
      $("#textarea-description").val(data.description);
    }

    if (data.parent_group.id) {
      const $option = $("<option>")
        .val(data.parent_group.id)
        .text(data.parent_group.name);
      $selectParentGroup.append($option);
      $selectParentGroup.val(data.parent_group.id).trigger("change");
    }

    for (const group of data.child_groups) {
      const $option = $("<option>").val(group.id).text(group.name);
      $selectChildGroups.append($option);
      $selectChildGroups.val(group.id).trigger("change");
    }

    // Fill in the permission checkboxes with the selected user's permissions
    $("#input-group-editteam").prop("checked", data.edit_team);
    $("#input-group-inviteuser").prop("checked", data.invite_user);
    $("#input-group-kickuser").prop("checked", data.kick_user);
    $("#input-group-createworldasteam").prop("checked", data.create_world_as_team);
  }
});
