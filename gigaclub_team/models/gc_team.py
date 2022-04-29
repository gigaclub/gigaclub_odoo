from odoo import api, fields, models


class GCTeam(models.Model):
    _name = "gc.team"
    _description = "GigaClub Team"

    name = fields.Char(required=True)
    description = fields.Text()

    permission_connector_ids = fields.One2many(
        comodel_name="gc.permission.connector", inverse_name="team_id", index=True
    )

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]

    @api.model
    def _check_access_gigaclub_team(self, player_uuid, permission):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_connector = user.permission_connector_ids.filtered("team_id")[:1]
        if team_connector:
            if team_connector.has_permission(permission):
                return team_connector.team_id
        return False

    # Status Codes:
    # 3: User already in team
    # 2: Team with name already exists
    # 1: Team could not be created
    # 0: Team created successfully
    @api.model
    def create_team(self, player_uuid, name, description=False):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if user.permission_connector_ids.mapped("team_id"):
            return 3
        if self.search_count([("name", "=ilike", name)]):
            return 2
        team_id = self.create(
            {
                "name": name,
                "description": description,
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
                                            "gigaclub_team.gc_permission_profile_template_default"  # noqa: B950
                                        ).id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )
        if not team_id:
            return 1
        return 0

    # Status Codes:
    # 1: No valid team found for this user
    # 0: Success
    @api.model
    def edit_team(self, player_uuid, new_name, new_description=False):
        team = self._check_access_gigaclub_team(player_uuid, "gigaclub_team.edit_team")
        if not team:
            return 1
        team.write(
            {
                "name": new_name,
                "description": new_description if new_description else team.description,
            }
        )
        return 0

    # Status Codes:
    # 1: User has no team
    # 0: Success
    @api.model
    def leave_team(self, player_uuid):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user_id.team_user_id and not user_id.team_manager_id:
            return 1
        if user_id.team_manager_id:
            user_id.team_manager_id = False
        elif user_id.team_user_id:
            user_id.team_user_id = False
        self.search([])._inverse_users()
        return 0

    # Status Codes:
    # 3: No valid team found for this user
    # 2: User to kick does not exist
    # 1: User is not member of team
    # 0: Success
    @api.model
    def kick_member(self, player_uuid, player_uuid_to_kick):
        team = self._check_access_gigaclub_team(
            player_uuid, "gigaclub_team.kick_member"
        )
        if not team:
            return 3
        user_to_kick = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_kick)]
        )
        if not user_to_kick:
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
            "name": team.name,
            "description": team.description,
            "user_ids": [{"mc_uuid": u.mc_uuid} for u in team.user_ids],
            "manager_ids": [{"mc_uuid": m.mc_uuid} for m in team.manager_ids],
        }

    @api.model
    def get_team_by_member(self, player_uuid):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = False
        if user.team_user_id:
            team = user.team_user_id
        elif user.team_manager_id:
            team = user.team_manager_id
        if team:
            return self.return_team(team)
        return False

    @api.model
    def get_all_teams(self):
        return [self.return_team(x) for x in self.search([])]

    @api.model
    def get_team(self, name):
        team = self.search([("name", "=ilike", name)])
        if team:
            return self.return_team(team)
        return []

    # Status Codes:
    # 3: No valid team found for this user
    # 2: User to invite not found
    # 1: User is already member of a team
    # 0: Success
    @api.model
    def invite_member(self, player_uuid, player_uuid_to_invite):
        team = self._check_access_gigaclub_team(
            player_uuid, "gigaclub_team.invite_member"
        )
        if not team:
            return 3
        user_to_invite = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_invite)]
        )
        if not user_to_invite:
            return 2
        if user_to_invite.permission_connector_ids.filtered("team_id"):
            return 1
        self.env["gc.request"].create(
            {
                "sender_id": f"{team._name},{team.id}",
                "receiver_id": f"{user_to_invite._name},{user_to_invite.id}",
                "state": "waiting",
            }
        )
        return 0

    # Status Codes:
    # 2: Team does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def accept_request(self, player_uuid, team_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = self.search([("name", "=ilike", team_name)])
        if not team:
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
        team.permission_connector_ids.create(
            {
                "user_id": user.id,
            }
        )
        return 0

    # Status Codes:
    # 2: Team does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def deny_request(self, player_uuid, team_name):
        user = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team = self.search([("name", "=ilike", team_name)])
        if not team:
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
