# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Copyright (C) 2021 arshsisodiya; Created by arshsisodiya

""" get random wallpapers from unsplash """

import asyncio
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.unsplash(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    msg_link = await event.get_reply_message()
    query = event.pattern_match.group(1)

    if msg_link:
        query = msg_link.text
        await event.edit("`Fetching awesome wallpaper from unsplash`")
    chat = "@awesomewallsbot"
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                await event.edit("Processing")
                response = await conv.get_response()
                send_query = await conv.send_message(query)
                await event.edit(f"Getting {query} wallpaper from unsplash.......")
                thumbnail = await conv.get_response()
                await event.edit("`Sending you Uncompressed High Quality Wall, Just Wait a bit....`")
                uncompressdfile = await conv.get_response()
                """- don't spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("Unblock `@awesomewallsbot` and retry")
                return
            await bot.send_file(event.chat_id, uncompressdfile, caption=thumbnail.text)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, send_query.id, thumbnail.id, uncompressdfile.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit("Error: `@awesomewallsbot` is not responding! please try again later.")

    CMD_HELP.update(
        {
            "unsplash": ".unsplash <query>"
                        "\nUsage: Get Awesome Wallpaper from Unsplash"
                        "\n\n.unsplash Random"
                        "\nUsage: To get Random wallpaper"

        }
    )
