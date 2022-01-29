# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Copyright (C) 2021 arshsisodiya https://github.com/arshsisodiya ; this module doesn't relate to Apple inc in any way ; 'shazam' is Copyrighted term of Apple.inc

import io
import os
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.shazam(?: |$)(.*)")
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await event.edit("```Reply to an audio message.```")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
      async with event.client.conversation(chat) as conv:
        try:
            await event.edit("```Identifying the song```")
            start_msg = await conv.send_message("/start")
            await conv.get_response()
            send_audio = await conv.send_message(reply_message)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await event.edit(
                    "An error while identifying the song. Try to use a 5-10s long audio message."
                )
            await event.edit("Wait just a sec...")
            result = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("```Please unblock (@auddbot) and try again```")
            return
        namem = f"**Song Name : **`{result.text.splitlines()[0]}`\
        \n\n**Details : **__{result.text.splitlines()[2]}__"
        await event.edit(namem)
        await event.client.delete_messages(
                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]
            )
    except TimeoutError:
        return await event.edit("`Error: `@auddbot` is not responding please try again later")

CMD_HELP.update(
    {
        "shazam": ">`.shazam <reply to voice/audio>" "\nUsage: Reverse search audio file using (@auddbot)"}
)
