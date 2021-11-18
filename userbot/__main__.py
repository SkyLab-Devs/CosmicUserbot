# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

from importlib import import_module
from sys import argv
from asyncio import sleep
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot, HEROKU_APP_NAME, HEROKU_API_KEY, repo_lenk
from userbot.modules import ALL_MODULES


INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(f"You are running Project Fizilion on {repo_lenk}")

LOGS.info(
    "Congratulations, your userbot is now running !! Test it by typing .alive / .on in any chat."
    "If you need assistance, head to https://t.me/ProjectFizilionChat")
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    print("HEROKU detected, sleeping for 5 minutes to prevent String Session Error")
    LOGS.info("HEROKU detected, sleeping for 5 minutes to prevent String Session Error")
    sleep(300)
    bot.run_until_disconnected()
bot.run_until_disconnected()
