#
# Python module which logs all the mentioned messages in Telegram Channel/Group.
#
# Copyright (C) 2022 PrajjuS <theprajjus@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#

import os
from userbot import bot, LOG_TAGGING, LOG_TAGGING_CHATID, LOGS
from userbot.events import register
from telethon import events
from telethon.tl.types import User

@bot.on(events.NewMessage(incoming=True, func=lambda event: (event.mentioned)))
async def on_tag(event):
    text = event.message.message or None
    msg_id = event.message.id
    sender = await event.get_sender()
    chat = await event.get_chat()
    user_id = sender.id
    first_name = sender.first_name
    chat_id = chat.id
    chat_name = chat.title
    try:
        username = sender.username
    except Exception:
        username = None
    try:
        chat_username = chat.username
    except Exception:
        chat_username = None
    if isinstance(sender, User) and (sender.bot or sender.verified):
        return
    if not LOG_TAGGING:
        return
    LOGS.info(f"Tag Event: {first_name}({user_id}) - {text}")
    LOG_TEXT = ""
    LOG_TEXT += "#USER_TAG_EVENT\n"
    if username is not None:
        LOG_TEXT += f"**- User:** [{first_name}](https://t.me/{username}) (`{user_id}`)\n"
    else:
        LOG_TEXT += f"**- User:** {first_name} (`{user_id}`)\n"
    if chat_username is not None:
        LOG_TEXT += f"**- Chat:** [{chat_name}](https://t.me/{chat_username}) (`{chat_id}`)\n"
        LOG_TEXT += f"**- Link:** [Here](https://t.me/{chat_username}/{msg_id})\n"
    else:
        LOG_TEXT += f"**- Chat:** {chat_name} (`{chat_id}`)\n"
        LOG_TEXT += f"**- Link:** [Here](https://t.me/c/{chat_id}/{msg_id})\n"
    LOG_TEXT += f"**- Text:** {text}"
    try:
        if event.photo or event.sticker or event.gif:
            media = await event.download_media()
            msg = await event.client.send_message(LOG_TAGGING_CHATID, file=media)
            await msg.reply(LOG_TEXT, link_preview=False)
            return os.remove(media)
        else:
            await event.client.send_message(LOG_TAGGING_CHATID, LOG_TEXT, link_preview=False)
    except Exception as e:
        LOGS.exception(e)
