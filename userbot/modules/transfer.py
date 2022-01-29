# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; © ElytrA8

""" a module for transferring files to many sites. """

import asyncio
import time
from userbot import CMD_HELP
from userbot.events import register


@register(pattern="^.transfer ?(.+?|) (?:)(arp|bit|cat|cow|gof|tmp|vim|wss|wet|flk|trs|lzs)")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Transfer in Progress")
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await bot.download_media(reply.media, Var.TEMP_DOWNLOAD_DIRECTORY)
    event.message.id
    CMD_WEB = {
        "arp": "transfer arp \"{}\"",
        "bit": "transfer bit \"{}\"",
        "cat": "transfer cat \"{}\"",
        "cow": "transfer cow \"{}\"",
        "gof": "transfer gof \"{}\"",
        "tmp": "transfer tmp \"{}\"",
        "vim": "transfer vim \"{}\"",
        "wss": "transfer wss \"{}\"",
        "wet": "transfer wet \"{}\"",
        "flk": "transfer flk \"{}\"",
        "trs": "transfer trs \"{}\"",
        "lzs": "transfer lzs \"{}\""}
    try:
        selected_one = CMD_WEB[selected_transfer].format(file_name)
    except KeyError:
        await event.edit("Invalid selected Transfer")
    cmd = selected_one
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f"{stdout.decode()}")
CMD_HELP.update({"transfer":
                 "`.transfer` (filepath) `arp`|`bit`|`cat`|`cow`|`gof`|`tmp`|`vim`|`wss`|`wet`|`flk`|`trs`|`lzs` and for information use guide"})
