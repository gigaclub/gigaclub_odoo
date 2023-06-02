from odoo import models


class GCUser(models.Model):
    _inherit = "gc.user"

    def merge_users(self, merge_user):
        self.ensure_one()
        self.update(
            {
                "permission_connector_ids": [
                    (4, permission_connector_id)
                    for permission_connector_id in merge_user.permission_connector_ids.ids
                ],
                "permission_profile_ids": [
                    (4, permission_profile_id)
                    for permission_profile_id in merge_user.permission_profile_ids.ids
                ],
                "permission_group_ids": [
                    (4, permission_group_id)
                    for permission_group_id in merge_user.permission_group_ids.ids
                ],
            }
        )
        mc_uuid = merge_user.mc_uuid
        merge_user.unlink()
        if self.env.context.get("get_mc_uuid_back", False):
            return mc_uuid
