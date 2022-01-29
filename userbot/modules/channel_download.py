# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.#Modified by @arshsisodiya #thanks to @Zero_cool7870 #https://github.com/arshsisodiya

""" a module for downloading files from channel. """

import os
import subprocess
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import media_type

@register(outgoing=True, pattern=r"^.getc(?: |$)([\s\S]*)")
async def get_media(event):
    chname = event.pattern_match.group(1)
    limit = int(chname.split(" ")[0])
    channel_username = str(chname.split(" ")[1])
    tempdir = os.path.join(TEMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        os.makedirs(tempdir)
    except BaseException:
        pass
    event = await event.edit(f"`Downloading Media From {channel_username} Channel from last {limit} messages.`")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From {channel_username} Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", tempdir), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", " ")
    output = output.replace("\\n'", " ")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to `{tempdir}`"
    )


@register(outgoing=True, pattern=r"^.geta(?: |$)([\s\S]*)")
async def get_media(event):
    channel_username = event.pattern_match.group(1)
    tempdir = os.path.join(TEMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        os.makedirs(tempdir)
    except BaseException:
        pass
    event = await event.edit(f"`Downloading All Media From `{channel_username}` Channel.`")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From `{channel_username}` Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", tempdir), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to `{tempdir}`"
    )

CMD_HELP.update({
    "channeldownload":
    ".geta <channel_username>"
    "\nUsage: will get all media from channel/group, tho there is limit of 3000 there to prevent API limits.."
    "\n\n.getc <number_of_messsages> <channel_username>"
    "\nUsage: download media only from given number of last messages."
    "\n\n Use .gd <tempdir path> to upload downloaded files to your google drive."

})
