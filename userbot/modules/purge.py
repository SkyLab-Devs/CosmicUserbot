# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.

""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.purge$")
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit("`I need a mesasge to start purging from.`")
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        f"`Fast purge complete!`\
        \nPurged {str(count)} messages",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID, "Purge of " + str(count) + " messages done successfully."
        )
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Purge complete!` Purged " + str(count) + " messages.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID, "Purge of " + str(count) + " messages done successfully."
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Deletion of message was successful"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well, I can't delete a message"
                )


@register(outgoing=True, pattern="^.edit")
async def editer(edit):
    """ For .editme command, edit your last message. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(
            BOTLOG_CHATID, "Edit query was executed successfully"
        )


@register(outgoing=True, pattern="^.sd")
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID, "sd query done successfully")

purgemsgs = {}

@register(outgoing=True, pattern="^\.(p|purge)(from$|to$)")
async def purgfromto(prgnew):
    reply = await prgnew.get_reply_message()
    if reply:
        if prgnew.pattern_match.group(2) == "from":
            await purgfrm(prgnew)
        elif prgnew.pattern_match.group(2) == "to":
            await purgto(prgnew)
    else:
        await prgnew.edit("Reply to a message to start purging")
        await sleep(4)
        await prgnew.delete()

async def purgfrm(prgfrm):
    prgstrtmsg = prgfrm.reply_to_msg_id
    purgemsgs[prgfrm.chat_id] = prgstrtmsg
    aa = await prgfrm.edit("This message has been selected as the purge start, reply to another message by .purgeto to delete between them.")
    await sleep(2)
    await aa.delete()

async def purgto(prgto):
    try:
        prgstrtmsg = purgemsgs[prgto.chat_id]
    except KeyError:
        aa = await prgto.edit("Reply to a message by .purgefrom first then use .purgeto")
        await sleep(2)
        await aa.delete()
        return
    try:
        chat = await prgto.get_input_chat()
        prgendmsg = prgto.reply_to_msg_id
        pmsgs = []
        msgz = 0
        async for msg in prgto.client.iter_messages(prgto.chat_id, min_id=(prgstrtmsg - 1), max_id=(prgendmsg + 1)):
            pmsgs.append(msg)
            msgz += 1
            pmsgs.append(prgto.reply_to_msg_id)
            if len(pmsgs) == 100:
                await prgto.client.delete_messages(chat, msgs)
                msgs = []
        if pmsgs:
            await prgto.client.delete_messages(chat, pmsgs)
            await prgto.delete()
        aaa = await prgto.reply(f"`Fast purge complete!`\nPurged {str(msgz)} messages")
        await sleep(5)
        await aaa.delete()
    except Exception as er:
        await prgto.edit(f"Umm an issue happened...\nERROR:\n`{str(er)}`")

CMD_HELP.update(
    {
        "purge": ".purge\
        \nUsage: Purges all messages starting from the reply.\
        \n\n.pfrom / .purgefrom\
        \nUsage: Marks the start of where to purge from\
        \n\n.pto / .purgeto\
        \nUsage: Marks the end of where to purge to.\nIt deletes the messages marked between purgefrom and purgeto\
        \n\m.purgeme <x>\
        \nUsage: Deletes x amount of your latest messages.\
        \n\n.del\
        \nUsage: Deletes the message you replied to.\
        \n\n.edit <newmessage>\
        \nUsage: Replace your last message with <newmessage>.\
        \n\n.sd <x> <message>\
        \nUsage: Creates a message that selfdestructs in x seconds.\
        \nKeep the seconds under 100 since it puts your bot to sleep."
    }
)
