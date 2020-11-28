# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

import pyfiglet

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.figlet(?: |$)(.*)")
async def figlet(fg):
    if fg.fwd_from:
        return
    CMD_FIG = {
        "SLANT": "slant",
        "3D": "3-d",
        "5LINE": "5lineoblique",
        "ALPHA": "alphabet",
        "BANNER": "banner3-D",
        "DOH": "doh",
        "ISO": "isometric1",
        "LETTER": "letters",
        "ALLIG": "alligator",
        "DOTM": "dotmatrix",
        "BUBBLE": "bubble",
        "BULB": "bulbhead",
        "DIGI": "digital",
    }
    ip = fg.pattern_match.group(1)
    input_str = ip.upper()
    if "." in input_str:
        text, cmd = input_str.split(".", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await fg.edit("`Please add some text to figlet`")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await fg.edit("`Invalid selected font.`")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await fg.edit("‌‌‎`{}`".format(result))

CMD_HELP.update(
    {
        "figlet": ".figlet"
        "\nUsage: Enhance ur text to strip line with anvil."
        "\n\nExample: `.figlet <Text> .<style>`"
        "\nSTYLE LIST: `slant`, `3D`, `5line`, `alpha`, `banner`, `doh`, `iso`, `letter`, `allig`, `dotm`, `bubble`, `bulb`, `digi`"
    }
)
