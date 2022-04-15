from userbot import CMD_HELP, bot
from userbot.events import register
from telethon.events import NewMessage


@register(outgoing=True, pattern="^\.fstat(?: |$)(.*)")
async def fstat(e: NewMessage.Event):
	tmsg = await e.reply("Checking...")
	try:
		rep = await e.get_reply_message()
	except:
		rep = None
	inp = e.pattern_match.group(1)
	if rep:
		user = rep.sender_id
		if inp:
			user = f"{rep.sender_id} {inp}"
	else:
		user = inp
	async with bot.conversation("@MissRose_bot") as conv:
		try:
			await conv.send_message(f"/fstat {user}")
		except Exception as err:
			await tmsg.edit(f"Cannot check the fstat\nReason:{err}")
		resp = await conv.get_response()
		if resp.message.startswith("Checking fbans for"):
			resp = await conv.get_edit()
		if resp.reply_markup:
			await resp.click(0)
			resp2 = await conv.get_response()
			await e.send_file(e.chat_id, resp2, caption=resp2.text)
			await tmsg.delete()
			return
		await tmsg.edit(resp.message)

CMD_HELP.update(
		{"fstat": "`.fstat <reply/mention/reply> <fed id>`\nUsage: Get the fstat of the user in @MissRose_bot."}
)
