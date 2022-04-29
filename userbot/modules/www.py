# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.

""" Userbot module containing commands related to the  Information Superhighway (yes, Internet). """

from datetime import datetime

from speedtest import Speedtest
from telethon import functions

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils import humanbytes

@register(outgoing=True, pattern=r"^\.speedtest$")
async def speedtest(event):
    """ For .speed command, use SpeedTest to check server speeds. """
    await event.edit("`Running speed test...`")

    test = Speedtest()
    await event.edit("`Choosing best server...`")
    test.get_best_server()
    await event.edit("`Testing download speed...`")
    test.download()
    await event.edit("`Testing upload speed...`")
    test.upload()
    result = test.results.dict()

    msg = (
        f"`--Started at {result['timestamp']}--`\n\n"
        f"`Ping:` `{result['ping']}`\n"
        f"`Upload:` `{humanbytes(result['upload'])}/s`\n"
        f"`Download:` `{humanbytes(result['download'])}/s`\n"
        f"`ISP:` `{result['client']['isp']}`\n"
        f"`Country:` `{result['client']['country']}`\n"
        f"`Name:` `{result['server']['name']}`\n"
        f"`Country:` `{result['server']['country']}`\n"
        f"`Sponsor:` `{result['server']['sponsor']}`\n\n"
    )

    await event.edit(msg)    

def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(
        f"Country : `{result.country}`\n"
        f"Nearest Datacenter : `{result.nearest_dc}`\n"
        f"This Datacenter : `{result.this_dc}`"
    )


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))

CMD_HELP.update(
    {
        "dc": ".dc\
    \nUsage: Finds the nearest datacenter from your server."
    }
)
CMD_HELP.update(
    {
        "ping": ".ping\
    \nUsage: Shows how long it takes to ping your bot."
    }
)
CMD_HELP.update(
    {
        "speedtest": ".speedtest\
            \nUsage: Does a speedtest and shows results."
    }
)
