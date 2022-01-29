# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.

""" module to get a list of chats where the user is an admin or the creator of the group. """

from typing import List
from enum import Enum

from ..import CMD_HELP
from ..events import register
from .telegraph import telegraph

class ChatStatus(Enum):
    owner = 'creator'
    admin   = 'admin_rights'

@register(outgoing=True, pattern=r"^\.(admin|owner)in$")
async def whereAmIAdminIn(e):
    text: List[str] = []
    stat = e.pattern_match.group(1)
    initMsg = f"Getting the chats I'm {stat.capitalize()} in..."
    msg = await e.edit(initMsg)
    diags = e.client.iter_dialogs()
    txt = f"<b>{stat.capitalize()}</b> in \n"
    async for c in diags:
        try:
            if c.is_group and getattr(c.entity, ChatStatus[stat].value):
                text.append(f"<br>- {getDialogLink(c)}")
        except AttributeError:
            None
    if len(text) > 20: # avoid sending a long message
        u_fname = f"List of chats where {(await e.client.get_me()).first_name} is {e.pattern_match.group(1).capitalize()} in:"
        tlink = "".join(iter(text))
        res = telegraph.create_page(title=u_fname, html_content=tlink)
        tmsg = "List too long, uploaded to [telegra.ph](https://telegra.ph/{})!".format(res["path"])
        return await e.edit(tmsg, link_preview=True)
    await msg.edit(txt + "\n".join(iter(text)), parse_mode="html")

def getDialogLink(dialog):
    return f'<a href="https://t.me/c/{dialog.entity.id}/99999999">{dialog.entity.title}</a>'

CMD_HELP.update({
    "mystats":
    ">`.adminin`"
    "\nUsage: Get the list if chats that you are admin in."
    "\n\n>`.ownerin`"
    "\nUsage: Get the list if chats that you created."
})
