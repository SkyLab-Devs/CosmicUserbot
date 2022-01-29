# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Modified and refractored by @PrajjuS

""" a module for making text stickers. """

import io
import os
import random
import textwrap
from emoji import get_emoji_regexp
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument

from userbot.events import register
from userbot.utils import edit_or_reply
from userbot import CMD_HELP 

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


@register(outgoing=True, pattern="^.stk(?: |$)(.*)")
async def sticklet(event):
    await event.edit("`Processing....`")
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    reply_message = event.message
    font_file_name = event.pattern_match.group(1)
    if not font_file_name:
        font_file_name = ""
    sticktext = event.pattern_match.group(1)
    if not sticktext:
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            sticktext = reply_message.message
        else:
            await edit_or_reply(event, "`Gib text or reply to any text..`")
            return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    await event.delete()
    sticktext = deEmojify(sticktext)
    sticktext = textwrap.wrap(sticktext, width=10)
    # converts back the list to a string
    sticktext = "\n".join(sticktext)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    FONT_FILE = await get_font_file(event.client, "@ProjectFizilionFonts")
    font = ImageFont.truetype(FONT_FILE, size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    image_stream = io.BytesIO()
    image_stream.name = "@ProjectFizilion.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    # finally, reply the sticker
    await event.client.send_file(
        event.chat_id,
        image_stream,
        caption="Fizilion's Sticklet",
        reply_to=event.message.reply_to_msg_id,
    )
    # cleanup
    try:
        os.remove(FONT_FILE)
    except BaseException:
        pass


async def get_font_file(client, channel_id, search_kw=""):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
        search=search_kw,
    )
    font_file_message = random.choice(font_file_message_s)
    return await client.download_media(font_file_message)

CMD_HELP.update({
        "sticklet":
        ".stk \
            \nUsage: Enhance ur sticker"
})
