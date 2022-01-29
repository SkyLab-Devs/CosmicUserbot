# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.

""" chat shifting module. """

import asyncio
from userbot.events import register
from userbot import CMD_HELP

@register(pattern=r"\.shift(?: |$)(.*)", outgoing=True)
async def _(e):
    x = e.pattern_match.group(1)
    z = await e.edit("`Processing..`")
    a, b = x.split("|")
    try:
        c = int(a)
    except Exception:
        try:
            c = (await e.client.get_entity(a)).id
        except Exception:
            await z.edit("`Invalid Channel`")
            return
    try:
        d = int(b)
    except Exception:
        try:
            d = (await e.client.get_entity(b)).id
        except Exception:
            await z.edit("`Invalid Channel`")
            return
    async for msg in e.client.iter_messages(int(c), reverse=True):
        try:
            await asyncio.sleep(0.7)
            await e.client.send_message(int(d), msg)
        except BaseException:
            pass
    await z.edit("`Done`")

CMD_HELP.update(
    {
        "shift":
        ">`.shift <from_chatid|to_chatid>`"
        "\nUsage: shifts all chats from one to another channel or group."
    }
)

