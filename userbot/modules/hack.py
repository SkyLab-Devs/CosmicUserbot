# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Ported from userge by @PrajjuS

""" meme module for userbot. """

from userbot.events import register
from userbot import CMD_HELP
import time
from asyncio import sleep 
from telethon import events , client , TelegramClient
from userbot.modules.admin import get_user_from_event

@register(outgoing=True, pattern="^.hack$")
async def hack_func(event):
    animation_chars = [
        "Connecting To Private Server \\",
        "Connecting To Private Server |",
        "Connecting To Private Server /",
        "Connecting To Private Server \\",
        "Connection Established ",
        "Target Selected",
        "Backdoor Found In Target",
        "Trying To Hack",
        "Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒",
        "Hacking... 70%\n█████████████████▒▒▒▒▒",
        "Hacking... 88%\n█████████████████████▒",
        "Hacking... 100%\n███████████████████████",
        "Preparing Data... 1%\n▒██████████████████████",
        "Preparing Data... 14%\n████▒██████████████████",
        "Preparing Data... 30%\n████████▒██████████████",
        "Preparing Data... 55%\n████████████▒██████████",
        "Preparing Data... 72%\n████████████████▒██████",
        "Preparing Data... 88%\n████████████████████▒██",
        "Prepared Data... 100%\n███████████████████████",
        "Uploading Data to Server... 12%\n███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Uploading Data to Server... 44%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "Uploading Data to Server... 68%\n███████████████▒▒▒▒▒▒▒▒",
        "Uploading Data to Server... 89%\n████████████████████▒▒▒",
        "Uploaded Data to Server... 100%\n███████████████████████",
        "**User Data Upload Completed:** Target's User Data Stored "
        "at `downloads/victim/telegram-authuser.data.sql`",
    ]
    hecked = (f"**Targeted Account Hacked**\n\nPay 69$ To hackerman\nTo Remove This Hack")
    max_ani = len(animation_chars)
    for i in range(max_ani):
        await sleep(2)
        await event.edit(animation_chars[i % max_ani])
    await event.edit(hecked)

    
CMD_HELP.update({
    "hack":
    "'.hack'"
    "\nUsage: Hackerman Meme"
    })
    
