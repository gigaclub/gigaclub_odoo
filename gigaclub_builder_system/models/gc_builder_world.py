from odoo import api, fields, models
from odoo.exceptions import ValidationError


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

    owner_id = fields.Many2one(comodel_name="gc.user", required=True)

    @api.model
    def _check_access_gigaclub_builder_system(self, player_uuid, world_id, permission):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        world = self.browse(world_id)
        if not world:
            return False
        if user == world.owner_id:
            return world
        world_connector = user.permission_connector_ids.filtered_domain(
            [
                ("world_id", "=", world_id),
            ]
        )[:1]
        if world_connector and world_connector.has_one_of_permissions(
            [permission, "gigaclub_builder_system.*", "*"]
        ):
            return world_connector.world_id
        return False

    # Status Codes:
    # 1: No Permission
    # 0: Success
    @api.model
    def create_as_user(self, player_uuid, task_id, name, world_type_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_builder_system.create_world", "gigaclub_builder_system.*", "*"]
        ):
            return 1
        task = self.env["project.task"].browse(task_id)
        world_type = self.env["gc.builder.world.type"].search(
            [("name", "=", world_type_name)], limit=1
        )
        if not world_type:
            world_type = self.env["gc.builder.world.type"].search(
                [("default", "=", True)], limit=1
            )
        self.create(
            {
                "name": name,
                "task_id": task.id,
                "world_type_id": world_type.id,
                "owner_id": user.id,
                "permission_connector_ids": [
                    (
                        0,
                        0,
                        {
                            "user_id": user.id,
                            "permission_profile_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "permission_profile_template_id": self.env.ref(
                                            "gigaclub_builder_system.gc_permission_profile_template_builder_system_default"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        return 0

    @api.model
    def create_as_team(self, player_uuid, team_id, task_id, name, world_type_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = self.env["gc.team"]._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.create_world_as_team"
        )
        if not team:
            return 1
        task = self.env["project.task"].browse(task_id)
        world_type = self.env["gc.builder.world.type"].search(
            [("name", "=ilike", world_type_name)], limit=1
        )
        if not world_type:
            world_type = self.env["gc.builder.world.type"].search(
                [("default", "=", True)], limit=1
            )
        permission_connectors = [
            (
                0,
                0,
                {
                    "team_id": team.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        for user in team.permission_connector_ids.mapped("user_id"):
            permission_connectors.append(
                (
                    0,
                    0,
                    {
                        "user_id": user.id,
                        "bound_to_team": True,
                        "permission_profile_ids": [
                            (
                                0,
                                0,
                                {
                                    "permission_profile_template_id": self.env.ref(
                                        "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                    ).id,
                                },
                            )
                        ],
                    },
                )
            )
        return self.create(
            {
                "name": name,
                "task_id": task.id,
                "world_type_id": world_type.id,
                "owner_id": user.id,
                "permission_connector_ids": permission_connectors,
            }
        ).id

    # Status Codes:
    # 4: No valid world found for this user
    # 3: User to invite not found
    # 2: User is already member of team
    # 1: Request already sent
    # 0: Success
    @api.model
    def invite_user_to_world(self, player_uuid, player_uuid_to_add, world_id):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.invite_user"
        )
        if not world:
            return 4
        user_to_invite = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_add)]
        )
        if not user_to_invite:
            return 3
        if user_to_invite.permission_connector_ids.filtered(
            lambda x: x.world_id == world
        ):
            return 2
        try:
            self.env["gc.request"].create(
                {
                    "sender_id": f"{world._name},{world.id}",
                    "receiver_id": f"{user_to_invite._name},{user_to_invite.id}",
                    "request_type": "member_or_team_to_world_invitation",
                    "state": "waiting",
                }
            )
        except ValidationError:
            return 1
        return 0

    # Status Codes:
    # 3: User has no permission to accept requests
    # 2: World does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def user_accept_request(self, player_uuid, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_builder_system.accept_request", "gigaclub_builder_system.*", "*"]
        ):
            return 3
        world = self.browse(world_id)
        if not world.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{world._name},{world.id}"),
                ("receiver_id", "=", f"{user._name},{user.id}"),
                ("request_type", "=", "member_or_team_to_world_invitation"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "accepted"
        world.permission_connector_ids |= self.env["gc.permission.connector"].create(
            {
                "user_id": user.id,
                "permission_profile_ids": [
                    (
                        0,
                        0,
                        {
                            "permission_profile_template_id": self.env.ref(
                                "gigaclub_builder_system.gc_permission_profile_template_builder_system_default"  # noqa: B950
                            ).id,
                        },
                    )
                ],
            }
        )
        return 0

    # Status Codes:
    # 3: User has no permission to reject requests
    # 2: World does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def user_deny_request(self, player_uuid, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_builder_system.deny_request", "gigaclub_builder_system.*", "*"]
        ):
            return 3
        world = self.browse(world_id)
        if not world.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{world._name},{world.id}"),
                ("receiver_id", "=", f"{user._name},{user.id}"),
                ("request_type", "=", "member_or_team_to_world_invitation"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "denied"
        return 0

    # Status Codes:
    # 4: No valid world found for this user
    # 3: Team to invite not found
    # 2: Team is already member of this world
    # 1: Request already sent
    # 0: Success
    @api.model
    def invite_team_to_world(self, player_uuid, team_id, world_id):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.invite_team"
        )
        if not world:
            return 4
        team_to_add = self.env["gc.team"].browse(team_id)
        if not team_to_add.exists():
            return 3
        if team_to_add.permission_connector_ids.filtered(lambda x: x.world_id == world):
            return 2
        try:
            self.env["gc.request"].create(
                {
                    "sender_id": f"{world._name},{world.id}",
                    "receiver_id": f"{team_to_add._name},{team_to_add.id}",
                    "request_type": "member_or_team_to_world_invitation",
                    "state": "waiting",
                }
            )
        except ValidationError:
            return 1
        return 0

    # Status Codes:
    # 4: User does not exist
    # 3: Team does not exist or user has no access
    # 2: World does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def team_accept_request(self, player_uuid, team_id, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.exists():
            return 4
        team = self.env["gc.team"]._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.accept_world_request_as_team"
        )
        if not team.exists():
            return 3
        world = self.browse(world_id)
        if not world.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{world._name},{world.id}"),
                ("receiver_id", "=", f"{team._name},{team.id}"),
                ("request_type", "=", "member_or_team_to_world_invitation"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "accepted"
        permission_connectors = [
            (
                0,
                0,
                {
                    "team_id": team.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                ).id,
                            },
                        )
                    ],
                },
            )
        ]
        for user in team.permission_connector_ids.mapped("user_id"):
            permission_connectors.append(
                (
                    0,
                    0,
                    {
                        "user_id": user.id,
                        "bound_to_team": True,
                        "permission_profile_ids": [
                            (
                                0,
                                0,
                                {
                                    "permission_profile_template_id": self.env.ref(
                                        "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                    ).id,
                                },
                            )
                        ],
                    },
                )
            )
        world.permission_connector_ids = permission_connectors
        return 0

    # Status Codes:
    # 4: User does not exist
    # 3: Team does not exist or user has no permission to reject requests
    # 2: World does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def team_deny_request(self, player_uuid, team_id, world_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.exists():
            return 4
        team = self.env["gc.team"]._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.deny_world_request_as_team"
        )
        if not team.exists():
            return 3
        world = self.browse(world_id)
        if not world.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{world._name},{world.id}"),
                ("receiver_id", "=", f"{team._name},{team.id}"),
                ("request_type", "=", "member_or_team_to_world_invitation"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "denied"
        return 0

    # Status Codes:
    # 1: World does not exist and user has no manager access to this world
    # 0: Success
    @api.model
    def remove_user_from_world(self, player_uuid, player_uuid_to_remove, world_id):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.remove_user"
        )
        if not world:
            return 1
        user_to_remove = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_remove)]
        )
        permission_connector = world.permission_connector_ids.filtered(
            lambda r: r.user_id == user_to_remove
        )
        if permission_connector:
            permission_connector.unlink()
        return 0

    # Status Codes:
    # 2: World does not exist or user has no manager access to this world
    # 1: Team does not exist
    # 0: Success
    @api.model
    def remove_team_from_world(self, player_uuid, team_id, world_id):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.remove_team"
        )
        if not world:
            return 2
        team_to_remove = self.env["gc.team"].browse(team_id)
        if not team_to_remove.exists():
            return 1
        team_permission_connector = world.permission_connector_ids.filtered(
            lambda r: r.team_id == team_to_remove
        )
        if team_permission_connector:
            team_users = team_to_remove.permission_connector_ids.mapped("user_id")
            user_permission_connectors = world.permission_connector_ids.filtered(
                lambda r: r.user_id in team_users and r.bound_to_team
            )
            if user_permission_connectors:
                user_permission_connectors.unlink()
            team_permission_connector.unlink()
        return 0

    # Status Codes:
    # 1: World does not exist
    # 0: Success
    @api.model
    def save_world(self, player_uuid, world_id, world_data):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.save_world"
        )
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
    def edit_world_type(self, player_uuid, world_id, world_type_name):
        world = self._check_access_gigaclub_builder_system(
            player_uuid, world_id, "gigaclub_builder_system.edit_world_type"
        )
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

    @api.model
    def return_world(self, world):
        return {
            "world_id": world.id,
            "name": world.name,
            "task_id": world.task_id.id,
            "world_type": world.world_type_id.name,
            "team_ids": [
                {
                    "id": t.id,
                    "name": t.name,
                    "permissions": t.permission_connector_ids.filtered(
                        lambda x: x.world_id == world
                    )
                    .get_permissions()
                    .mapped("name"),
                }
                for t in world.permission_connector_ids.mapped("team_id")
            ],
            "user_ids": [
                {
                    "mc_uuid": u.mc_uuid,
                    "permissions": u.permission_connector_ids.filtered(
                        lambda x: x.world_id == world
                    )
                    .get_permissions()
                    .mapped("name"),
                }
                for u in world.permission_connector_ids.mapped("user_id")
            ],
            "owner_id": world.owner_id.mc_uuid,
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
