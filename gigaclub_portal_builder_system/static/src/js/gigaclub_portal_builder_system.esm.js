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

$("#deleteWorldConfirmModal").on("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const worldId = button.getAttribute("data-bs-world_id");
  window.currentWorldId = worldId;
});
