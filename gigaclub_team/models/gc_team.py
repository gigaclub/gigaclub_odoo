from odoo import api, fields, models


class GCTeam(models.Model):
    _name = "gc.team"
    _description = "GigaClub Team"

    name = fields.Char(required=True)
    description = fields.Text()

    user_ids = fields.One2many(
        comodel_name="gc.user", inverse_name="team_user_id", inverse="_inverse_users"
    )
    manager_ids = fields.One2many(
        comodel_name="gc.user", inverse_name="team_manager_id", inverse="_inverse_users"
    )

    _sql_constraints = [("name_unique", "UNIQUE(name)", "name must be unique!")]

    def _inverse_users(self):
        for rec in self:
            if len(rec.manager_ids) == 0 and len(rec.user_ids) > 0:
                user_id = rec.user_ids[0]
                rec.user_ids -= user_id
                rec.manager_ids |= user_id
            if not rec.user_ids and not rec.manager_ids:
                rec.unlink()

    # Status Codes:
    # 3: User already in team
    # 2: Team with name already exists
    # 1: Team could not be created
    # 0: Team created successfully
    @api.model
    def create_team(self, player_uuid, name, description=False):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if user_id.team_user_id or user_id.team_manager_id:
            return 3
        if self.search_count([("name", "=ilike", name)]):
            return 2
        team_id = self.create(
            {"name": name, "description": description, "manager_ids": [(4, user_id.id)]}
        )
        if not team_id:
            return 1
        return 0

    # Status Codes:
    # 3: User has no team
    # 2: Team does not exist
    # 1: User is not manager of this team
    # 0: Success
    @api.model
    def edit_team(self, player_uuid, name, new_name, new_description=False):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        if not user_id.team_user_id and not user_id.team_manager_id:
            return 3
        team_id = self.search([("name", "=ilike", name)])
        if not team_id:
            return 2
        if user_id not in team_id.manager_ids:
            return 1
        team_id.write(
            {
                "name": new_name,
                "description": new_description
                if new_description
                else team_id.description,
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
    # 3: Team does not exist
    # 2: User is not manager
    # 1: User is not user of this team
    # 0: Success
    @api.model
    def add_member(self, player_uuid, player_uuid_to_add):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = user_id.team_user_id or user_id.team_manager_id
        if not team_id:
            return 3
        if user_id not in team_id.manager_ids:
            return 2
        user_id_to_add = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_add)]
        )
        if user_id_to_add in team_id.user_ids:
            return 1
        team_id.user_ids |= user_id_to_add
        return 0

    # Status Codes:
    # 3: Team does not exist
    # 2: User is not manager
    # 1: User is not user of this team
    # 0: Success
    @api.model
    def kick_member(self, player_uuid, player_uuid_to_kick):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = user_id.team_user_id or user_id.team_manager_id
        if not team_id:
            return 3
        if user_id not in team_id.manager_ids:
            return 2
        user_id_to_kick = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_kick)]
        )
        if user_id_to_kick not in team_id.user_ids:
            return 1
        team_id.user_ids = [(3, user_id_to_kick.id)]
        return 0

    # Status Codes:
    # 4: Team does not exist
    # 3: User is not manager
    # 2: User to kick is not in a team
    # 1: User to kick is not in this team
    # 0: Success
    @api.model
    def promote_member(self, player_uuid, player_uuid_to_promote):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = user_id.team_user_id or user_id.team_manager_id
        if not team_id:
            return 4
        if user_id not in team_id.manager_ids:
            return 3
        user_id_to_promote = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_promote)]
        )
        if not user_id_to_promote.team_user_id:
            return 2
        if user_id_to_promote.team_user_id != team_id:
            return 1
        team_id.user_ids -= user_id_to_promote
        team_id.manager_ids |= user_id_to_promote
        return 0

    # Status Codes:
    # 4: Team does not exist
    # 3: User is not manager
    # 2: User to kick is not a team
    # 1: User to kick is not in this team
    # 0: Success
    @api.model
    def demote_member(self, player_uuid, player_uuid_to_demote):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = user_id.team_user_id or user_id.team_manager_id
        if not team_id:
            return 4
        if user_id not in team_id.manager_ids:
            return 3
        user_id_to_demote = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_demote)]
        )
        if not user_id_to_demote.team_manager_id:
            return 2
        if user_id_to_demote.team_manager_id != team_id:
            return 1
        team_id.manager_ids -= user_id_to_demote
        team_id.user_ids |= user_id_to_demote
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
    # 3: Team does not exist
    # 2: User is not manager
    # 1: User is already member of this team
    # 0: Success
    @api.model
    def invite_member(self, player_uuid, player_uuid_to_invite):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = user_id.team_user_id or user_id.team_manager_id
        if not team_id:
            return 3
        if user_id not in team_id.manager_ids:
            return 2
        user_id_to_invite = self.env["gc.user"].search(
            [("mc_uuid", "=", player_uuid_to_invite)]
        )
        if user_id_to_invite in team_id.user_ids | team_id.manager_ids:
            return 1
        self.env["gc.request"].create(
            {
                "sender_id": f"{team_id._name},{team_id.id}",
                "receiver_id": f"{user_id_to_invite._name},{user_id_to_invite.id}",
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
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = self.search([("name", "=ilike", team_name)])
        if not team_id:
            return 2
        request_id = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{team_id._name},{team_id.id}"),
                ("receiver_id", "=", f"{user_id._name},{user_id.id}"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request_id:
            return 1
        request_id.state = "accepted"
        team_id.user_ids |= user_id
        return 0

    # Status Codes:
    # 2: Team does not exist
    # 1: Request does not exist
    # 0: Success
    @api.model
    def deny_request(self, player_uuid, team_name):
        user_id = self.env["gc.user"].search([("mc_uuid", "=", player_uuid)])
        team_id = self.search([("name", "=ilike", team_name)])
        if not team_id:
            return 2
        request_id = self.env["gc.request"].search(
            [
                ("sender_id", "=", f"{team_id._name},{team_id.id}"),
                ("receiver_id", "=", f"{user_id._name},{user_id.id}"),
                ("state", "=", "waiting"),
            ],
            limit=1,
        )
        if not request_id:
            return 1
        request_id.state = "denied"
        return 0
