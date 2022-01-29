# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Copyright (C) 2021 arshsisodiya

""" speech to text converter module. """

import asyncio
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.stt(?: |$)(.*)")
async def _(event):
    "To recognize a image."
    if not event.reply_to_msg_id:
        return await event.edit("Reply to any user's media message.")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await event.edit(event, "reply to media file")
    chat = "@voicybot"
    if reply_message.sender.bot:
        return await event.edit(event, "Reply to actual users message.")
    await event.edit("identifying the media")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            await event.edit("voice recognition is initiated.....")
            speech = await event.client.send_message(chat, reply_message)
            response = await conv.get_response()
            await sleep(4)
            result = await conv.get_response()
            """- don't spam notif -"""
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("`Unblock `@voicybot` and retry`")
            return
        text = f"`{result.text.splitlines()[0]}`"
        await event.edit(text)
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, response.id, result.id, speech.id]
        )


CMD_HELP.update(
    {
        "stt": ".speech to text "
                 "\nUsage: Reply to a audio file to convert it into text "
                 "using `@voicybot`"
    }
)

