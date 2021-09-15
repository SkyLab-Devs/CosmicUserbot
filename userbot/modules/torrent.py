# Copyright (C) 2021 arshsisodiya
#https://github.com/arshsisodiya
#https://twitter.com/arshsisodiya

#Created by arshsisodiya for ProjectHelios

import asyncio
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ts(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    msg_link = await event.get_reply_message()
    d_link = event.pattern_match.group(1)

    if msg_link:
        d_link = msg_link.text
    chat = "@TorrentHuntBot"
    await event.edit("Searching....")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(d_link)
                await sleep(3)
                torrent = await conv.get_response()
                """- don't spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock `@TorrentHuntBot` and retry`")
                return
            await event.client.send_message(event.chat_id, torrent,)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, msg.id, torrent.id]
            )
            await event.edit("`reply .get <link_id> to get magnet link`")
            await sleep (4)
            await event.delete()
    except TimeoutError:
        return await event.edit("`Error: @TorrentHuntBot is not responding please try again later")


@register(outgoing=True, pattern=r"^\.tos(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    msg_link = await event.get_reply_message()
    d_link = event.pattern_match.group(1)

    if msg_link:
        d_link = msg_link.text
    chat = "@TorrentHuntBot"
    await event.edit("Fetching magnet link...")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(d_link)
                await sleep(2)
                torrent = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock `@TorrentHuntBot` and retry`")
                return
            await event.client.send_message(event.chat_id, torrent,)
            await event.client.delete_messages(
                conv.chat_id, [msg.id, torrent.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit("`Error: @TorrentHuntBot is not responding please try again later")

CMD_HELP.update(
        {
            "torrent": ".ts \
            \nUsage: Search Torrents \
            \n\n.tos \
            \nUsage:reply to getLink<id> to get Magnet Link\n"

        }
    )
