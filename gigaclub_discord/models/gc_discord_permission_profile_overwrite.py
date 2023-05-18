from odoo import api, fields, models


class GCDiscordPermissionProfileOverwrite(models.Model):
    _name = "gc.discord.permission.profile.overwrite"
    _description = "GigaClub Discord Permission Profile overwrite"

    def _selection_permission(self):
        return [("yes", "Yes"), ("no", "No")]

    overwrite_entity_id = fields.Reference(
        selection=[("gc.discord.role", "gc.discord.role"), ("gc.user", "gc.user")],
        required=True,
    )

    channel_id = fields.Many2one(comodel_name="gc.discord.channel", index=True)
    category_id = fields.Many2one(comodel_name="gc.discord.category", index=True)

    administrator = fields.Selection(selection=_selection_permission)
    create_instant_invite = fields.Selection(selection=_selection_permission)
    kick_members = fields.Selection(selection=_selection_permission)
    ban_members = fields.Selection(selection=_selection_permission)
    manage_channels = fields.Selection(selection=_selection_permission)
    manage_guild = fields.Selection(selection=_selection_permission)
    add_reactions = fields.Selection(selection=_selection_permission)
    view_audit_log = fields.Selection(selection=_selection_permission)
    priority_speaker = fields.Selection(selection=_selection_permission)
    stream = fields.Selection(selection=_selection_permission)
    read_messages = fields.Selection(selection=_selection_permission)
    send_messages = fields.Selection(selection=_selection_permission)
    send_tts_messages = fields.Selection(selection=_selection_permission)
    manage_messages = fields.Selection(selection=_selection_permission)
    embed_links = fields.Selection(selection=_selection_permission)
    attach_files = fields.Selection(selection=_selection_permission)
    read_message_history = fields.Selection(selection=_selection_permission)
    mention_everyone = fields.Selection(selection=_selection_permission)
    external_emojis = fields.Selection(selection=_selection_permission)
    view_guild_insights = fields.Selection(selection=_selection_permission)
    connect = fields.Selection(selection=_selection_permission)
    speak = fields.Selection(selection=_selection_permission)
    mute_members = fields.Selection(selection=_selection_permission)
    deafen_members = fields.Selection(selection=_selection_permission)
    move_members = fields.Selection(selection=_selection_permission)
    use_voice_activation = fields.Selection(selection=_selection_permission)
    change_nickname = fields.Selection(selection=_selection_permission)
    manage_nicknames = fields.Selection(selection=_selection_permission)
    manage_roles = fields.Selection(selection=_selection_permission)
    manage_webhooks = fields.Selection(selection=_selection_permission)
    manage_emojis = fields.Selection(selection=_selection_permission)
    request_to_speak = fields.Selection(selection=_selection_permission)
    view_channel = fields.Selection(selection=_selection_permission)
    use_external_emojis = fields.Selection(selection=_selection_permission)
    manage_permissions = fields.Selection(selection=_selection_permission)
    manage_emojis_and_stickers = fields.Selection(selection=_selection_permission)
    use_application_commands = fields.Selection(selection=_selection_permission)
    manage_events = fields.Selection(selection=_selection_permission)
    manage_threads = fields.Selection(selection=_selection_permission)
    create_public_threads = fields.Selection(selection=_selection_permission)
    create_private_threads = fields.Selection(selection=_selection_permission)
    send_messages_in_threads = fields.Selection(selection=_selection_permission)
    external_stickers = fields.Selection(selection=_selection_permission)
    use_external_stickers = fields.Selection(selection=_selection_permission)
    use_embedded_activities = fields.Selection(selection=_selection_permission)
    moderate_members = fields.Selection(selection=_selection_permission)
    use_soundboard = fields.Selection(selection=_selection_permission)
    use_external_sounds = fields.Selection(selection=_selection_permission)
    send_voice_messages = fields.Selection(selection=_selection_permission)

    @api.model
    def get_permission_value(self, value):
        if value == "yes":
            return True
        if value == "no":
            return False
        return None
