# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for interacting with dogbin(https://del.dog)"""

import os

from requests import exceptions, get, post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DOGBIN_URL = "https://pasty.lus.pm/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .paste command, pastes the text directly to dogbin. """
    dogbin_final_url = ""
    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not match and not reply_id:
        await pstl.edit("`Elon Musk said I cannot paste void.`")
        return

    if match:
        message = match
    elif reply_id:
        message = await pstl.get_reply_message()
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    # Pasty
    await pstl.edit("`Pasting text . . .`")
    dta={"content":message}
    resp = post(DOGBIN_URL + "api/v2/pastes", json=dta)
    print(resp.content)

    if resp.status_code in (200,201):
        response = resp.json()
        key = response["id"]
        dogbin_final_url = DOGBIN_URL + key
        print(response)
        reply_text = (
            "`Pasted successfully!`\n\n"
            f"[Pasty URL]({dogbin_final_url})\n"
            f"[Pasty RAW URL]({dogbin_final_url+'/raw'})"
        )
    else:
        reply_text = "`Failed to reach Pasty`"

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            f"Paste query was executed successfully",
        )

CMD_HELP.update(
    {
        "paste": ".paste <text/reply>\
\nUsage: Create a paste or a shortened url using pasty (https://pasty.lus.pm//)"
    }
)
