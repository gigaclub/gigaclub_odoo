from odoo import api, fields, models


class GCBuilderWorld(models.Model):
    _name = "gc.builder.world"
    _description = "GigaClub Builder World"

    def _default_world_type_id(self):
        return self.env["gc.builder.world.type"].search(
            [("default", "=", True)], limit=1
        )

    name = fields.Char()
    world_attachment_id = fields.Many2one(comodel_name="ir.attachment")
    world_type_id = fields.Many2one(
        comodel_name="gc.builder.world.type", default=_default_world_type_id
    )

    task_id = fields.Many2one(comodel_name="project.task", required=True, index=True)

    permission_connector_ids = fields.One2many(
        comodel_name="gc.permission.connector", inverse_name="world_id"
    )

    @api.model
    def _check_access_gigaclub_builder_system(self, player_uuid, world_id, permission):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world_connector = user.permission_connector_ids.filtered_domain(
            [
                ("world_id", "=", world_id),
            ]
        )[:1]
        if world_connector and world_connector.has_permission(permission):
            return world_connector.world_id
        return False

    @api.model
    def create_as_user(self, player_uuid, task_id, name, world_type_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        task = self.env["project.task"].browse(task_id)
        world_type = self.env["gc.builder.world.type"].search(
            [("name", "=ilike", world_type_name)], limit=1
        )
        if not world_type:
            world_type = self.env["gc.builder.world.type"].search(
                [("default", "=", True)], limit=1
            )
        return self.create(
            {
                "name": name,
                "task_id": task.id,
                "world_type_id": world_type.id,
                "user_manager_ids": [(4, user.id)],
            }
        ).id

    @api.model
    def create_as_team(self, player_uuid, task_id, name, world_type_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = False
        if user.team_manager_id:
            team = user.team_manager_id
        elif user.team_user_id:
            team = user.team_user_id
        task = self.env["project.task"].browse(task_id)
        world_type = self.env["gc.builder.world.type"].search(
            [("name", "=ilike", world_type_name)], limit=1
        )
        if not world_type:
            world_type = self.env["gc.builder.world.type"].search(
                [("default", "=", True)], limit=1
            )
        return self.create(
            {
                "name": name,
                "task_id": task.id,
                "world_type_id": world_type.id,
                "team_manager_ids": [(4, team.id)],
            }
        ).id

    # Status Codes:
    # 2: World does not exist
    # 1: User has no manager access to this world
    # 0: Success
    @api.model
    def add_user_to_world(self, player_uuid, player_uuid_to_add, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world = self.browse(world_id)
        if not world:
            return 2
        if (
            user not in world.user_manager_ids
            and user not in world.team_manager_ids.mapped("user_ids")
            and user not in world.team_manager_ids.mapped("manager_ids")
        ):
            return 1
        user_to_add = self.env["gc.user"].search([("mc_uuid", "=", player_uuid_to_add)])
        world.user_ids |= user_to_add
        return 0

    # Status Codes:
    # 3: World does not exist
    # 2: User has no manager access to this world
    # 1: Team does not exist
    # 0: Success
    @api.model
    def add_team_to_world(self, player_uuid, team_name, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world = self.browse(world_id)
        if not world:
            return 3
        if (
            user not in world.user_manager_ids
            and user not in world.team_manager_ids.mapped("user_ids")
            and user not in world.team_manager_ids.mapped("manager_ids")
        ):
            return 2
        team_to_add = self.env["gc.team"].search([("name", "=ilike", team_name)])
        if not team_to_add:
            return 1
        world.team_ids |= team_to_add
        return 0

    # Status Codes:
    # 2: World does not exist
    # 1: User has no manager access to this world
    # 0: Success
    @api.model
    def remove_user_from_world(self, player_uuid, player_uuid_to_remove, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world = self.browse(world_id)
        if not world:
            return 2
        if (
            user not in world.user_manager_ids
            and user not in world.team_manager_ids.mapped("user_ids")
            and user not in world.team_manager_ids.mapped("manager_ids")
        ):
            return 1
        user_to_remove = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_remove)]
        )
        world.user_ids = [(3, user_to_remove.id)]
        return 0

    # Status Codes:
    # 3: World does not exist
    # 2: User has no manager access to this world
    # 1: Team does not exist
    # 0: Success
    @api.model
    def remove_team_from_world(self, player_uuid, team_name, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world = self.browse(world_id)
        if not world:
            return 3
        if (
            user not in world.user_manager_ids
            and user not in world.team_manager_ids.mapped("user_ids")
            and user not in world.team_manager_ids.mapped("manager_ids")
        ):
            return 2
        team_to_remove = self.env["gc.team"].search([("name", "=ilike", team_name)])
        if not team_to_remove:
            return 1
        world.team_ids = [(3, team_to_remove.id)]
        return 0

    # Status Codes:
    # 1: World does not exist
    # 0: Success
    @api.model
    def save_world(self, world_id, world_data):
        world = self.browse(world_id)
        if not world:
            return 1
        world.world_attachment_id = self.env["ir.attachment"].create(
            {
                "name": world.name,
                "datas": world_data,
            }
        )
        return 0

    # Status Codes:
    # 1: World does not exist
    # 0: Success
    @api.model
    def edit_world_type(self, world_id, world_type_name):
        world = self.browse(world_id)
        if not world:
            return 1
        world_type = self.env["gc.builder.world.type"].search(
            [("name", "=ilike", world_type_name)], limit=1
        )
        world.world_type_id = world_type
        return 0

    @api.model
    def get_world_data(self, world_id):
        world = self.browse(world_id)
        # TODO: This is not the final version.
        return world.world_attachment_id.datas

    def return_world(self, world):
        return {
            "world_id": world.id,
            "name": world.name,
            "task_id": world.task_id.id,
            "world_type": world.world_type_id.name,
            "team_ids": [
                {"name": t.name}
                for t in world.permission_connector_ids.mapped("team_id")
            ],
            "user_ids": [
                {"mc_uuid": u.mc_uuid}
                for u in world.permission_connector_ids.mapped("user_id")
            ],
        }

    @api.model
    def get_all_worlds(self):
        return [self.return_world(x) for x in self.search([])]

    @api.model
    def get_world(self, world_id):
        world = self.browse(world_id)
        if world:
            return self.return_world(world)
        return []
