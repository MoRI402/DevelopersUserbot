# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from pyrogram.errors import UserAdminInvalid
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters

from _pyrogram import app, CMD_HELP
from _pyrogram.helpers.pyrohelper import get_arg, get_args
from _pyrogram.helpers.adminhelpers import CheckAdmin
from config import PREFIX

CMD_HELP.update(
    {
        "Admin Tools": """
 **Admin Tools** 
  `ban` -> Bans user indefinitely.
  `unban` -> Unbans the user.
  `promote` [optional title] -> Promotes a user.
  `demote` _> Demotes a user.
  `mute` -> Mutes user indefinitely.
  `unmute` -> Unmutes the user.
  `kick` -> Kicks the user out of the group.
  `gmute` -> Doesn't lets a user speak(even admins).
  `ungmute` -> Inverse of what gmute does.
  `pin` -> pins a message.
  `del` -> delete a message.
  `purge` -> purge message(s)
  `invite` -> add user to chat.
"""
    }
)


@app.on_message(filters.command("ban", PREFIX) & filters.me)
async def ban_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await message.edit("User is Missing `CanRestrictMembers` Rights to use this command")
                return
        try:
            get_user = await app.get_users(user)
            await app.kick_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"Banned {get_user.first_name} from the chat.")
        except Exception as e:
            await message.edit(f"Unable to Ban the User \n\nError: {e}")
    else:
        await message.edit("User need to be Admin to use this command")


@app.on_message(filters.command("unban", PREFIX) & filters.me)
async def unban(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await message.edit("You need to specify a user by replying, or providing a username or user id...!")
                return
        try:
            get_user = await app.get_users(user)
            await app.unban_chat_member(chat_id=message.chat.id, user_id=get_user.id)
            await message.edit(f"Unbanned {get_user.first_name} from the chat.")

        except Exception as e:
            await message.edit(f"Unable to UnBan the User \n\nError: {e}")
    else:
        await message.edit("User need to be Admin to use this command")

# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@app.on_message(filters.command("mute", PREFIX) & filters.me)
async def mute_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await message.edit("You need to specify a user by replying, or providing a username or user id...!")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=mute_permission,
            )
            await message.edit(f"{get_user.first_name} has been muted.**")
        except Exception as e:
            await message.edit(f"Unable to Mute the User \n\nError: {e}")
    else:
        await message.edit("User need to be Admin to use this command")


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@app.on_message(filters.command("unmute", PREFIX) & filters.me)
async def unmute(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await message.edit("You need to specify a user by replying, or providing a username or user id...!")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=unmute_permissions,
            )
            await message.edit(f"**{get_user.first_name} was unmuted.**")
        except Exception as e:
            await message.edit(f"Unable to UnMute the User \n\nError: {e}")
    else:
        await message.edit("User need to be Admin to use this command")


@app.on_message(filters.command("kick", PREFIX) & filters.me)
async def kick_user(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await message.edit("You need to specify a user by replying, or providing a username or user id...!")
                return
        try:
            get_user = await app.get_users(user)
            await app.kick_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"**Kicked {get_user.first_name} from the chat.**")
        except Exception as e:
            await message.edit(f"Unable to Kick the User \n\nError: {e}")
    else:
        await message.edit("User need to be Admin to use this command")


@app.on_message(filters.command("pin", PREFIX) & filters.me)
async def pin_message(_, message: Message):
    # First of all check if its a group or not
    if message.chat.type in ["group", "supergroup"]:
        # Here lies the sanity checks
        admins = await app.get_chat_members(
            message.chat.id, filter=ChatMemberFilters.ADMINISTRATORS
        )
        admin_ids = [user.user.id for user in admins]
        me = await app.get_me()

        # If you are an admin
        if me.id in admin_ids:
            # If you replied to a message so that we can pin it.
            if message.reply_to_message:
                disable_notification = True

                # Let me see if you want to notify everyone. People are gonna hate you for this...
                if len(message.command) >= 2 and message.command[1] in [
                    "alert",
                    "notify",
                    "loud",
                ]:
                    disable_notification = False

                # Pin the fucking message.
                await app.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id,
                    disable_notification=disable_notification,
                )
                await message.edit("`Pinned message!`")
            else:
                # You didn't reply to a message and we can't pin anything. ffs
                await message.edit(
                    "`Reply to a message so that I can pin the god damned thing...`"
                )
        else:
            # You have no business running this command.
            await message.edit("User need to be Admin to use this command")
    else:
        # Are you fucking dumb this is not a group ffs.
        await message.edit("`This is not a place where I can Pin Messages`")

    # And of course delete your lame attempt at changing the group picture.
    # RIP you.
    # You're probably gonna get ridiculed by everyone in the group for your failed attempt.
    # RIP.
    await asyncio.sleep(3)
    await message.delete()


@app.on_message(filters.command("promote", PREFIX) & filters.me)
async def promote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("User need to be Admin to use this command")
        return
    title = "Admin"
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
        title = str(get_arg(message))
    else:
        args = get_args(message)
        if not args:
            await message.edit("User is Missing `CanPromoteMembers` Rights to use this Command")
            return
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(message.chat.id, user, can_pin_messages=True)
        await message.edit(
            f"Successfully Promoted {get_user.first_name} with title {title}"
        )
    except Exception as e:
        await message.edit(f"{e}")
    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass


@app.on_message(filters.command("demote", PREFIX) & filters.me)
async def demote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("User need to be Admin to use this Command")
        return
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("User is Missing `CanPromoteMembers` Rights to use this Command")
            return
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(
            message.chat.id,
            user,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_edit_messages=False,
            can_invite_users=False,
            can_promote_members=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_post_messages=False,
        )
        await message.edit(
            f"Successfully Demoted {get_user.first_name}"
        )
    except Exception as e:
        await message.edit(f"{e}")


@app.on_message(filters.command("invite", PREFIX) & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**I can't invite no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"Successfully added {get_user.first_name} to this chat")
    except Exception as e:
        await message.edit(f"{e}")