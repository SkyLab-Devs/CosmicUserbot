# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; All Thenks goes to Emily ( The creater of This Plugin) from ftg userbot; ported by arshsisodiya

""" profile pic scrapping module. """

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern=r"^\.d(p|isplaypic)(?: |$)(.*)")
@register(outgoing=True, pattern=r"^\.p(p|profilepic)(?: |$)(.*)")
async def _(event):
    "To get user or group profile pic"
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
        await event.edit("Downloading profile picture of the replied user")
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
        await event.edit("Downloading profile picture of the current chat")
    if uid.strip() == "":
        await event.edit("Downloading current profile picture of the user")
        uid = 1
        if int(uid) > (len(photos)):
            return await event.edit("`No photo found of this NIBBA / NIBBI. Now u Die!`"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "all":
        await event.edit("Downloading all profile pictures of the user")
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await event.edit("`This user has no photos to show you`")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await event.edit(
                    event, "```number Invalid!``` **Are you Comedy Me ?**"
                )
                return
        except BaseException:
            await event.edit("`Are you comedy me ?`")
            return
        if int(uid) > (len(photos)):
            return await edit_delere(
                event, "`No photo found of this NIBBA / NIBBI. Now u Die!`"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()

CMD_HELP.update(
    {"displaypic": ">`.dp` \nUsage: Reply to a user to get his profile pic \ If you don't reply to any specific user \
        then the bot will get the chat profile pic"
             "\n\n>`dp"
             "\nUsage: download current picture of the user."
             "\n\n>`dp all"
             "\nUsage: download all profile pictures of the user."
             "\n\n>`dp <number>`"
             "\nUsage: download the <number>th profile picture of the user "
             "\n\n>`pp"
             "\nUsage: download current picture of the user."
             "\n\n>`pp all"
             "\nUsage: download all profile pictures of the user."
             "\n\n>`pp <number>`"
             "\nUsage: download the <number>th profile picture of the user "

     }
)
