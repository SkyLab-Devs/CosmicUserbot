# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.;#Copyright @arshsisodiya

""" a module for converting images to pdf. """

import asyncio
from asyncio.exceptions import TimeoutError
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.pdf(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("Reply to any text/image.")
    reply_message = await event.get_reply_message()
    chat = "@office2pdf_bot"
    await event.edit("Converting into PDF..")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(reply_message)
                convert = await conv.send_message("/ready2conv")
                cnfrm = await conv.get_response()
                editfilename = await conv.send_message("Yes")
                enterfilename = await conv.get_response()
                filename = await conv.send_message("Project Fizilion")
                started = await conv.get_response()
                pdf = await conv.get_response()
                """- don't spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock @office2pdf_bot and retry")
                return
            await event.client.send_message(event.chat_id, pdf)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, msg.id, started.id, filename.id, editfilename.id, enterfilename.id, cnfrm.id, pdf.id, convert.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
                "Error: Sorry @office2pdf_bot is not responding please try again later ")

CMD_HELP.update(
    {
        "pdf": ".pdf"
        "\nUsage: Convert text/image into a PDF file "
    }
)

