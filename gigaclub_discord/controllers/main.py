import asyncio
import threading

import discord
from discord.ext import commands
from odoo import _, api, http, registry
from odoo.http import request


class MainController(http.Controller):
    class MyBot(commands.Bot):
        def __init__(self, command_prefix, env):
            commands.Bot.__init__(self, command_prefix=command_prefix)
            self.env = env

        async def on_ready(self):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    company_id = new_env.user.company_id or new_env[
                        "res.company"
                    ].browse(1)
                    company_id.gc_discord_server_status = "started"
                    for guild in self.guilds:
                        if not new_env["gc.user"].search_count(
                            [("discord_uuid", "=", str(guild.owner_id))]
                        ):
                            new_env["gc.user"].create(
                                {"discord_uuid": str(guild.owner_id)}
                            )
                        for member in guild.members:
                            if not new_env["gc.user"].search_count(
                                [("discord_uuid", "=", str(member.id))]
                            ):
                                new_env["gc.user"].create(
                                    {"discord_uuid": str(member.id)}
                                )
                        for channel in guild.channels:
                            if isinstance(channel, discord.channel.CategoryChannel):
                                await self.register_category(channel)
                            else:
                                await self.register_channel(channel)
                        for role in guild.roles:
                            await self.register_role(role)

        async def on_member_join(self, member):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.user"].search_count(
                        [("discord_uuid", "=", str(member.id))]
                    ):
                        new_env["gc.user"].create({"discord_uuid": str(member.id)})
                        user = new_env["gc.user"].search(
                            [("discord_uuid", "=", member.id)]
                        )
                        events = new_env["gc.discord.event"].search(
                            [("event_type", "=", "guild_join")]
                        )
                        for event in events:
                            actions = new_env["gc.discord.action"].search(
                                [("start_event_id", "=", event.id)]
                            )
                            for action in actions:
                                event_worker_ids = new_env["gc.discord.event.worker"]
                                for event in action.event_ids:
                                    event_worker_ids |= event.user_action and event
                                worker_id = new_env["gc.discord.action.worker"].create(
                                    {
                                        "action_id": action.id,
                                        "event_worker_ids": [
                                            [6, 0, event_worker_ids.ids]
                                        ],
                                    }
                                )
                                worker_id.event_worker_ids[0].done = True
                                worker_id.event_worker_ids[1].current = True
                        event_workers = new_env["gc.discord.event.worker"].search(
                            [
                                ("current", "=", True),
                                ("event_id.event_type", "=", "guild_join"),
                                ("user_id", "=", user.id),
                            ]
                        )
                        for event in event_workers:
                            event.done = True
                            event.current = False

        async def register_role(self, role):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.role"].search_count(
                        [("role_id", "=", str(role.id))]
                    ):
                        role_id = new_env["gc.discord.role"].create(
                            {
                                "name": role.name,
                                "role_id": str(role.id),
                                "hoist": role.hoist,
                                "position": role.position,
                                "managed": role.managed,
                                "mentionable": role.mentionable,
                            }
                        )
                        member_ids = []
                        for member in role.members:
                            user_id = new_env["gc.user"].search(
                                [("discord_uuid", "=", str(member.id))], limit=1
                            )
                            if user_id:
                                member_ids.append(user_id.id)
                        role_id.user_ids = [[6, 0, member_ids]]
                        perm = role.permissions
                        permission_profile_id = role_id.permission_profile_id.create(
                            {
                                "name": role.name,
                                "administrator": perm.administrator,
                                "create_instant_invite": perm.create_instant_invite,
                                "kick_members": perm.kick_members,
                                "ban_members": perm.ban_members,
                                "manage_channels": perm.manage_channels,
                                "manage_guild": perm.manage_guild,
                                "add_reactions": perm.add_reactions,
                                "view_audit_log": perm.view_audit_log,
                                "priority_speaker": perm.priority_speaker,
                                "stream": perm.stream,
                                "read_messages": perm.read_messages,
                                "send_messages": perm.send_messages,
                                "send_tts_messages": perm.send_tts_messages,
                                "manage_messages": perm.manage_messages,
                                "embed_links": perm.embed_links,
                                "attach_files": perm.attach_files,
                                "read_message_history": perm.read_message_history,
                                "mention_everyone": perm.mention_everyone,
                                "external_emojis": perm.external_emojis,
                                "view_guild_insights": perm.view_guild_insights,
                                "connect": perm.connect,
                                "speak": perm.speak,
                                "mute_members": perm.mute_members,
                                "deafen_members": perm.deafen_members,
                                "move_members": perm.move_members,
                                "use_voice_activation": perm.use_voice_activation,
                                "change_nickname": perm.change_nickname,
                                "manage_nicknames": perm.manage_nicknames,
                                "manage_roles": perm.manage_roles,
                                "manage_webhooks": perm.manage_webhooks,
                                "manage_emojis": perm.manage_emojis,
                                "use_slash_commands": perm.use_slash_commands,
                                "request_to_speak": perm.request_to_speak,
                            }
                        )
                        role_id.permission_profile_id = permission_profile_id
                    else:
                        role_id = new_env["gc.discord.role"].search(
                            [("role_id", "=", str(role.id))], limit=1
                        )
                        perm = role_id.permission_profile_id
                        permissions = discord.Permissions(
                            administrator=perm.administrator,
                            create_instant_invite=perm.create_instant_invite,
                            kick_members=perm.kick_members,
                            ban_members=perm.ban_members,
                            manage_channels=perm.manage_channels,
                            manage_guild=perm.manage_guild,
                            add_reactions=perm.add_reactions,
                            view_audit_log=perm.view_audit_log,
                            priority_speaker=perm.priority_speaker,
                            stream=perm.stream,
                            read_messages=perm.read_messages,
                            send_messages=perm.send_messages,
                            send_tts_messages=perm.send_tts_messages,
                            manage_messages=perm.manage_messages,
                            embed_links=perm.embed_links,
                            attach_files=perm.attach_files,
                            read_message_history=perm.read_message_history,
                            mention_everyone=perm.mention_everyone,
                            external_emojis=perm.external_emojis,
                            view_guild_insights=perm.view_guild_insights,
                            connect=perm.connect,
                            speak=perm.speak,
                            mute_members=perm.mute_members,
                            deafen_members=perm.deafen_members,
                            move_members=perm.move_members,
                            use_voice_activation=perm.use_voice_activation,
                            change_nickname=perm.change_nickname,
                            manage_nicknames=perm.manage_nicknames,
                            manage_roles=perm.manage_roles,
                            manage_webhooks=perm.manage_webhooks,
                            manage_emojis=perm.manage_emojis,
                            use_slash_commands=perm.use_slash_commands,
                            request_to_speak=perm.request_to_speak,
                        )
                        await role.edit(
                            name=role_id.name,
                            hoist=role_id.hoist,
                            mentionable=role_id.mentionable,
                            position=role_id.position,
                            permissions=permissions,
                        )

        async def register_category(self, channel):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.category"].search_count(
                        [("discord_channel_uuid", "=", str(channel.id))]
                    ):
                        new_env["gc.discord.category"].create(
                            {
                                "discord_channel_uuid": str(channel.id),
                                "name": str(channel.name),
                            }
                        )
                    else:
                        category_id = new_env["gc.discord.category"].search(
                            [("discord_channel_uuid", "=", str(channel.id))]
                        )
                        await channel.edit(name=category_id.name)

        async def register_channel(self, channel):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if not new_env["gc.discord.channel"].search_count(
                        [("discord_channel_uuid", "=", str(channel.id))]
                    ):
                        channel_type = False
                        if isinstance(channel, discord.channel.TextChannel):
                            channel_type = "text"
                            if channel.is_news():
                                channel_type = "announcement"
                        elif isinstance(channel, discord.channel.VoiceChannel):
                            channel_type = "voice"
                        elif isinstance(channel, discord.channel.StageChannel):
                            channel_type = "stage"
                        if type:
                            create_dict = {
                                "discord_channel_uuid": str(channel.id),
                                "name": str(channel.name),
                                "type": channel_type,
                            }
                            if channel.category:
                                await self.register_category(channel.category)
                                category_id = new_env["gc.discord.category"].search(
                                    [
                                        (
                                            "discord_channel_uuid",
                                            "=",
                                            str(channel.category.id),
                                        )
                                    ]
                                )
                                if category_id:
                                    create_dict["category_id"] = category_id.id
                            new_env["gc.discord.channel"].create(create_dict)
                    else:
                        channel_id = new_env["gc.discord.channel"].search(
                            [("discord_channel_uuid", "=", str(channel.id))]
                        )
                        if channel_id:
                            await channel.edit(name=channel_id.name)
                            if channel_id.category_id:
                                category = self.get_channel(
                                    int(channel_id.category_id.discord_channel_uuid)
                                )
                                await channel.edit(category=category)
                            else:
                                await channel.edit(category=None)

        async def refresh_categories_and_channels(self):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    company_id = new_env.user.company_id or new_env[
                        "res.company"
                    ].browse(1)
                    if company_id.gc_discord_reload:
                        for guild in self.guilds:
                            if guild.id == int(company_id.gc_discord_server_id):
                                for role in guild.roles:
                                    await self.register_role(role)
                                for channel in guild.channels:
                                    if isinstance(
                                        channel, discord.channel.CategoryChannel
                                    ):
                                        await self.register_category(channel)
                                    else:
                                        await self.register_channel(channel)
                                    await self.create_not_created_channels(guild)
                                    await self.create_not_created_categories(guild)

        async def create_not_created_channels(self, guild):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    not_created_channel_ids = new_env["gc.discord.channel"].search(
                        [("discord_channel_uuid", "=", False)]
                    )
                    if not_created_channel_ids:
                        for channel_id in not_created_channel_ids:
                            category = False
                            channel = False
                            if (
                                channel_id.category_id
                                and not channel_id.category_id.discord_channel_uuid
                            ):
                                category = await guild.create_category(
                                    name=channel_id.category_id.name
                                )
                                channel_id.category_id.discord_channel_uuid = str(
                                    category.id
                                )
                            elif channel_id.category_id:
                                category = await guild.get_channel(
                                    int(channel_id.category_id.discord_channel_uuid)
                                )
                            if channel_id.type == "text":
                                channel = await guild.create_text_channel(
                                    name=channel_id.name,
                                    category=category,
                                )
                            elif channel_id.type == "voice":
                                channel = await guild.create_voice_channel(
                                    name=channel_id.name,
                                    category=category,
                                )
                            elif channel_id.type == "stage":
                                channel = await guild.create_stage_channel(
                                    name=channel_id.name,
                                    category=category,
                                )
                            elif channel_id.type == "announcement":
                                channel = await guild.create_text_channel(
                                    name=channel_id.name,
                                    category=category,
                                    type=discord.ChannelType.news,
                                )
                            new_env["gc.discord.channel"].write(
                                {"discord_channel_uuid": str(channel.id)}
                            )

        async def create_not_created_categories(self, guild):
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    not_created_category_ids = new_env["gc.discord.category"].search(
                        [("discord_channel_uuid", "=", False)]
                    )
                    if not_created_category_ids:
                        for category_id in not_created_category_ids:
                            category = await guild.create_category(
                                name=category_id.name
                            )
                            category_id.discord_channel_uuid = str(category.id)

        async def on_message(self, message):
            if message.author == self.user:
                return
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    if message.channel == discord.DMChannel:
                        user = new_env["gc.user"].search(
                            [("discord_uuid", "=", message.author.id)]
                        )
                        events = new_env["gc.discord.event"].search(
                            [("event_type", "=", "get_private_message")]
                        )
                        for event in events:
                            actions = new_env["gc.discord.action"].search(
                                [("start_event_id", "=", event.id)]
                            )
                            for action in actions:
                                event_worker_ids = new_env["gc.discord.event.worker"]
                                for event in action.event_ids:
                                    event_worker_ids |= event.user_action and event
                                worker_id = new_env["gc.discord.action.worker"].create(
                                    {
                                        "action_id": action.id,
                                        "event_worker_ids": [
                                            [6, 0, event_worker_ids.ids]
                                        ],
                                    }
                                )
                                worker_id.event_worker_ids[0].done = True
                                worker_id.event_worker_ids[1].current = True
                        event_workers = new_env["gc.discord.event.worker"].search(
                            [
                                ("current", "=", True),
                                ("event_id.event_type", "=", "get_private_message"),
                                ("user_id", "=", user.id),
                            ]
                        )
                        for event in event_workers:
                            event.done = True
                            event.current = False

        async def shutdown(self):
            await self.logout()

        async def send_message(self, user_id, message):
            user = self.get_user(user_id)
            await self.send_message(user, message)

    async def bot_async_start(self, gc_discord_bot_token):
        await self.client.start(gc_discord_bot_token)

    def bot_loop_start(self, loop):
        loop.run_forever()

    @http.route(["/discordbot/start"], type="http", method=["POST"], csrf=False)
    def start_discord_bot(self):
        company_id = request.env.user.company_id or request.env["res.company"].browse(1)
        if (
            company_id.gc_discord_bot_token
            and company_id.gc_discord_server_status
            and company_id.gc_discord_server_status == "stopped"
        ):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.client = self.MyBot(command_prefix="!", env=request.env)
            loop.create_task(self.bot_async_start(company_id.gc_discord_bot_token))
            bot_thread = threading.Thread(target=self.bot_loop_start, args=(loop,))
            bot_thread.start()
        else:
            raise Exception(
                _("Bot is Started or Discord Bot Token or Discord Server ID not set!")
            )
        return "<script>window.close()</script>"

    @http.route(["/discordbot/stop"], type="http", method=["POST"], csrf=False)
    def stop_discord_bot(self):
        company_id = request.env.user.company_id or request.env["res.company"].browse(1)
        if (
            company_id.gc_discord_bot_token
            and company_id.gc_discord_server_status
            and company_id.gc_discord_server_status == "started"
        ):
            try:
                asyncio.run(self.client.logout())
                del self.client
            except Exception:
                pass
            company_id.gc_discord_server_status = "stopped"
        else:
            raise Exception(
                _("Bot is Stopped or Discord Bot Token or Discord Server ID not set!")
            )
        return "<script>window.close()</script>"

    @http.route(["/discordbot/reload"], type="http", method=["POST"], csrf=False)
    def reload_discord_bot(self):
        self.stop_discord_bot()
        self.start_discord_bot()
        asyncio.run(self.client.refresh_categories_and_channels())
        return "<script>window.close()</script>"

    @http.route(
        ["/discordbot/event/<int:event_id>"], type="http", method=["POST"], csrf=False
    )
    def discord_bot_event(self, event_id):
        event = request.env["gc.discord.event.worker"].browse(event_id)
        if event.event_id.event_type == "send_private_message":
            user = event.gc_user_id.discord_uuid
            event.gc_user_id = user
