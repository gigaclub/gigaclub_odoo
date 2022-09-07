from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GCTeam(models.Model):
    _name = "gc.team"
    _description = "GigaClub Team"

    name = fields.Char(required=True)
    description = fields.Text()

    permission_connector_ids = fields.One2many(
        comodel_name="gc.permission.connector", inverse_name="team_id"
    )
    possible_permission_group_ids = fields.Many2many(comodel_name="gc.permission.group")

    owner_id = fields.Many2one(comodel_name="gc.user", required=True)

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for rec in records:
            user_group = self.env["gc.permission.group"].create(
                {
                    "name": "User",
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_user"
                                ).id
                            },
                        )
                    ],
                }
            )
            manager_group = self.env["gc.permission.group"].create(
                {
                    "name": "Manager",
                    "parent_group_id": user_group.id,
                    "permission_profile_ids": [
                        (
                            0,
                            0,
                            {
                                "permission_profile_template_id": self.env.ref(
                                    "gigaclub_team.gc_permission_profile_template_team_manager"
                                ).id
                            },
                        )
                    ],
                }
            )
            rec.possible_permission_group_ids = user_group | manager_group
        return records

    @api.model
    def _check_access_gigaclub_team(self, player_uuid, team_id, permission):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = self.browse(team_id)
        if not team.exists():
            return False
        if user == team.owner_id:
            return team
        team_connector = user.permission_connector_ids.filtered_domain(
            [("team_id", "=", team.id)]
        )[:1]
        if team_connector and team_connector.has_one_of_permissions(
            [permission, "gigaclub_team.*", "*"]
        ):
            return team_connector.team_id
        return False

    # Status Codes:
    # 3: User has no access to create a team
    # 2: Team with name already exists
    # 1: Team could not be created
    # 0: Team created successfully
    @api.model
    def create_team(self, player_uuid, name, description=False):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_team.create_team", "gigaclub_team.*", "*"]
        ):
            return 3
        if self.search_count([("name", "=ilike", name)]):
            return 2
        team = self.create(
            {
                "name": name,
                "description": description,
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
                                            "gigaclub_team.gc_permission_profile_template_team_default"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        if not team:
            return 1
        return 0

    # Status Codes:
    # 1: No valid team found for this user
    # 0: Success
    @api.model
    def edit_team(self, player_uuid, team_id, new_name=False, new_description=False):
        team = self._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.edit_team"
        )
        if not team:
            return 1
        team.write(
            {
                "name": new_name or team.name,
                "description": new_description or team.description,
            }
        )
        return 0

    # Status Codes:
    # 2: User has no permission to leave teams
    # 1: User has no team
    # 0: Success
    @api.model
    def leave_team(self, player_uuid, team_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = self.browse(team_id)
        if not user.has_one_of_permissions(
            ["gigaclub_team.leave_team", "gigaclub_team.*", "*"]
        ):
            return 2
        team_connector_to_leave = user.permission_connector_ids.filtered_domain(
            [("team_id", "=", team.id)]
        )[:1]
        if not team_connector_to_leave:
            return 1
        team_connector_to_leave.unlink()
        if user == team.owner_id:
            new_owner = team.permission_connector_ids.mapped("user_id")[:1]
            if new_owner:
                team.owner_id = new_owner
            else:
                team.unlink()
        return 0

    # Status Codes:
    # 4: No valid team found for this user
    # 3: User to kick does not exist
    # 2: Not allowed to kick owner
    # 1: User is not member of team
    # 0: Success
    @api.model
    def kick_member(self, player_uuid, team_id, player_uuid_to_kick):
        team = self._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.kick_member"
        )
        if not team:
            return 4
        user_to_kick = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_kick)]
        )
        if not user_to_kick:
            return 3
        if user_to_kick == team.owner_id:
            return 2
        user_to_kick_team_connector = user_to_kick.permission_connector_ids.filtered(
            lambda x: x.team_id == team
        )[:1]
        if not user_to_kick_team_connector:
            return 1
        user_to_kick_team_connector.unlink()
        return 0

    def return_team(self, team):
        return {
            "id": team.id,
            "name": team.name,
            "description": team.description or "",
            "owner_id": team.owner_id.mc_uuid,
            "user_ids": [
                {"mc_uuid": u.mc_uuid}
                for u in team.permission_connector_ids.mapped("user_id")
            ],
        }

    @api.model
    def get_teams_by_member(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        teams = user.permission_connector_ids.mapped("team_id")
        if teams:
            return self.get_teams(teams)
        return self.env["gc.team"]

    @api.model
    def get_all_teams(self):
        return [self.return_team(x) for x in self.search([])]

    @api.model
    def get_teams(self, teams):
        return [self.return_team(x) for x in teams]

    @api.model
    def get_team(self, team_id):
        team = self.browse(team_id)
        if team.exists():
            return self.return_team(team)
        return []

    # Status Codes:
    # 4: No valid team found for this user
    # 3: User to invite not found
    # 2: User is already member of team
    # 1: Request already sent
    # 0: Success
    @api.model
    def invite_member(self, player_uuid, team_id, player_uuid_to_invite):
        team = self._check_access_gigaclub_team(
            player_uuid, team_id, "gigaclub_team.invite_member"
        )
        if not team:
            return 4
        user_to_invite = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_invite)]
        )
        if not user_to_invite:
            return 3
        if user_to_invite.permission_connector_ids.filtered(
            lambda x: x.team_id == team
        ):
            return 2
        try:
            self.env["gc.request"].create(
                {
                    "sender_id": f"{team._name},{team.id}",
                    "receiver_id": f"{user_to_invite._name},{user_to_invite.id}",
                    "state": "waiting",
                }
            )
        except ValidationError:
            return 1
        return 0

    # Status Codes:
    # 3: User has no permission to accept requests
    # 2: Team does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def accept_request(self, player_uuid, team_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_team.accept_request", "gigaclub_team.*", "*"]
        ):
            return 3
        team = self.browse(team_id)
        if not team.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{team._name},{team.id}"),
                ("receiver_id", "=", f"{user._name},{user.id}"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "accepted"
        team.permission_connector_ids |= self.env["gc.permission.connector"].create(
            {
                "user_id": user.id,
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
            }
        )
        return 0

    # Status Codes:
    # 3: User has no permission to reject requests
    # 2: Team does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def deny_request(self, player_uuid, team_id):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user.has_one_of_permissions(
            ["gigaclub_team.deny_request", "gigaclub_team.*", "*"]
        ):
            return 3
        team = self.browse(team_id)
        if not team.exists():
            return 2
        request = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{team._name},{team.id}"),
                ("receiver_id", "=", f"{user._name},{user.id}"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request:
            return 1
        request.state = "denied"
        return 0
