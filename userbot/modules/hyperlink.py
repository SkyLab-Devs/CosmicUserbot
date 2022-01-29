# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License. ; by priyam karla

""" hyperlink creator module. """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^.hl(.*)")
async def _(event):
    if event.fwd_from:
        return
    string = event.pattern_match.group(1)
    strings = string.split()
    link = strings[-1]
    strings = strings[:-1]
    string = " ".join(strings)
    output = f"[{string}]({link})"
    await event.edit(output)

CMD_HELP.update({
    "hl":
    "Use :- .hl <word> <link>"})
