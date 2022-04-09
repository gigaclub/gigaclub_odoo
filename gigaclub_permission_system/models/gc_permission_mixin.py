from odoo import api, models


class GCPermissionMixin(models.AbstractModel):
    _name = "gc.permission.mixin"
    _description = "GigaClub Permission Mixin"

    @api.model
    def create_permission_group(self):
        pass

    @api.model
    def delete_permission_group(self):
        pass

    @api.model
    def add_user_to_permission_group(self):
        pass

    @api.model
    def remove_user_from_permission_group(self):
        pass

    @api.model
    def create_permission_profile_for_user(self):
        pass

    @api.model
    def edit_permission_profile_of_user(self):
        pass

    @api.model
    def delete_permission_profile_from_user(self):
        pass

    @api.model
    def create_permission_profile_for_group(self):
        pass

    @api.model
    def edit_permission_profile_of_group(self):
        pass

    @api.model
    def delete_permission_profile_from_group(self):
        pass
