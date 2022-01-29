# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; Modified by Senpai-sama-afk/@SenpaiAF

""" Userbot module containing various scrapers. """

import asyncio
import json
import os
import glob
import re
import shutil
import time
from asyncio import sleep
from urllib.parse import quote_plus
import asyncurban
from bs4 import BeautifulSoup
from emoji import get_emoji_regexp
from google_trans_new import LANGUAGES, google_translator
from googletrans import Translator
from gpytranslate import Translator as tr
from requests import get
from duckduckgo_search import ddg
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.modules.upload_download import get_video_thumb
from userbot.utils import chrome, duckduckgoscraper, progress
from userbot.utils.FastTelethon import upload_file

CARBONLANG = "auto"
TTS_LANG = "en"
TRT_LANG = os.environ.get("TRT_LANG") or "en"
TEMP_DOWNLOAD_DIRECTORY = "/Fizilion/.bin/"


@register(outgoing=True, pattern=r"^\.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Language for carbon.now.sh set to {CARBONLANG}")

@register(outgoing=True, pattern=r"^\.carbon")
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    await e.edit("`Processing...`")
    CARBON = "https://carbon.now.sh/?l={lang}&code={code}"
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    await e.edit("`Processing...\n25%`")
    file_path = TEMP_DOWNLOAD_DIRECTORY + "carbon.png"
    if os.path.isfile(file_path):
        os.remove(file_path)
    url = CARBON.format(code=code, lang=CARBONLANG)
    driver = await chrome()
    driver.get(url)
    await e.edit("`Processing..\n50%`")
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": TEMP_DOWNLOAD_DIRECTORY },
    }
    driver.execute("send_command", params)
    driver.find_element_by_css_selector('[data-cy="quick-export-button"]').click()
    await e.edit("`Processing...\n75%`")
    # Waiting for downloading
    while not os.path.isfile(file_path):
        await sleep(0.5)
    await e.edit("`Processing...\n100%`")
    await e.edit("`Uploading...`")
    await e.client.send_file(
        e.chat_id,
        file_path,
        caption=(
            "Made using [Carbon](https://carbon.now.sh/about/),"
            "\na project by [Dawn Labs](https://dawnlabs.io/)"
        ),
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove(file_path)
    driver.quit()
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg



@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("`Processing...\n please wait for a moment...`")
    query = event.pattern_match.group(1)
    scraper = duckduckgoscraper.DuckDuckGoScraper()
    
    #The out directory
    os.system("mkdir -p /tmp/out/images")
    out = ("/tmp/out/images")
    
    if 'query' not in locals():
        await event.edit("Please specify a query to get images,\n like .img duck")
    else:
        #TODO: add a limit to the images being downloaded
        scraper.scrape(query,1,out)
        await asyncio.sleep(4)
        files = glob.glob("/tmp/out/images/*.jpg")
        await event.client.send_file(
            await event.client.get_input_entity(event.chat_id), files
                )
        await event.delete()
        os.system("rm -rf /tmp/out/images")

@register(outgoing=True, pattern=r"^\.currency ([\d\.]+) ([a-zA-Z]+) ([a-zA-Z]+)")
async def moni(event):
    c_from_val = float(event.pattern_match.group(1))
    c_from = (event.pattern_match.group(2)).upper()
    c_to = (event.pattern_match.group(3)).upper()
    try:
        response = get(
            "https://api.ratesapi.io/api/latest",
            params={"base": c_from, "symbols": c_to},
        ).json()
    except Exception:
        await event.edit("`Error: API is down.`")
        return
    if "error" in response:
        await event.edit(
            "`This seems to be some alien currency, which I can't convert right now.`"
        )
        return
    c_to_val = round(c_from_val * response["rates"][c_to], 2)
    await event.edit(f"`{c_from_val} {c_from} = {c_to_val} {c_to}`")

@register(outgoing=True, pattern=r"^.ddg(?: |$)(.*)")
async def gsearch(q_event):
    """For .ddg command, do a DuckDuckGo search."""
    textx = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)

    if query:
        pass
    elif textx:
        query = textx.text
    else:
        await q_event.edit(
            "`Pass a query as an argument or reply " "to a message for DuckDuckGo search!`"
        )
        return

    msg = ""
    await q_event.edit("`Searching...`")
    try:
        rst = ddg(query)
        i = 1
        while i <=5:
            result = rst[i]
            msg += f"{i}: [{result['title']}]({result['href']})\n"
            msg += f"{result['body']}\n\n"
            i += 1
        await q_event.edit(msg)
        if BOTLOG:
            await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
            )    
    except Exception as e:
        await q_event.edit(f"An error: {e} occured, report it to support group")

@register(outgoing=True, pattern=r"^\.wiki(?: |$)(.*)")
async def wiki(wiki_q):
    """ For .wiki command, fetch content from Wikipedia. """

    if wiki_q.is_reply and not wiki_q.pattern_match.group(1):
        match = await wiki_q.get_reply_message()
        match = str(match.message)
    else:
        match = str(wiki_q.pattern_match.group(1))

    if not match:
        return await wiki_q.edit("`Reply to a message or pass a query to search!`")

    await wiki_q.edit("`Processing...`")

    try:
        summary(match)
    except DisambiguationError as error:
        return await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
    except PageError as pageerror:
        return await wiki_q.edit(f"Page not found.\n\n{pageerror}")
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption=r"`Output too large, sending as file`",
        )
        if os.path.exists("output.txt"):
            return os.remove("output.txt")
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query `{match}` was executed successfully"
        )

@register(outgoing=True, pattern=r"^\.ipinfo(?: |$)(.*)")
async def ipinfo(event):
    #Thanks to https://ipinfo.io for this api
    ip = event.pattern_match.group(1)
    #os.system("curl ipinfo.io/{0} --silent > /Fizilion/ip.txt".format(ip))
    
    if ip:
        info = json.loads(get(f"https://ipinfo.io/{ip}").text)
    else:
        info = json.loads(get(f"https://ipinfo.io/").text)

    if "error" in info:
        await event.edit("Invalid IP address")        
    elif "country" in info:
        await event.edit(
            "`IP CREDENTIALS FOUND!`\n\n"
            f"•`IP Address     : {info['ip']}`\n"
            f"•`City           : {info['city']}`\n"
            f"•`State          : {info['region']}`\n"
            f"•`Country        : {info['country']}`\n"
            f"•`Lat/Long       : {info['loc']}`\n"
            f"•`Organisation   : {info['org']}`\n"
            f"•`Pin code       : {info['postal']}`\n"
            f"•`Time Zone      : {info['timezone']}`\n\n"
            "`This info might not be 100% Accurate`"
       )
    elif "bogon" in info:
        await event.edit(
            "`Some IP addresses and IP ranges are reserved for special use, such as for local or private networks, and should not appear on the  public internet. These reserved ranges, along with other IP ranges that haven’t yet been allocated and therefore also shouldn’t appear on the public internet are sometimes known as bogons\n So your ip: {0} is a bogon ip`".format(info["ip"])
        )
    else:
        await event.edit("Invalid Information Provided")
        
@register(outgoing=True, pattern=r"^\.ud(?: |$)(.*)")
async def urban_dict(event):
    """Output the definition of a word from Urban Dictionary"""

    if event.is_reply and not event.pattern_match.group(1):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(1))

    if not query:
        return await event.edit("`Reply to a message or pass a query to search!`")

    await event.edit("Processing...")
    ud = asyncurban.UrbanDictionary()
    template = "`Query: `{}\n\n`Definition: `{}\n\n`Example:\n`{}"

    try:
        definition = await ud.get_word(query)
    except asyncurban.UrbanException as e:
        return await event.edit("**Error:** {e}.")

    result = template.format(
        definition.word,
        definition.definition,
        definition.example)

    if len(result) >= 4096:
        await event.edit("`Output too large, sending as file...`")
        with open("output.txt", "w+") as file:
            file.write(
                "Query: "
                + definition.word
                + "\n\nMeaning: "
                + definition.definition
                + "Example: \n"
                + definition.example
            )
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            caption=f"Urban Dictionary's definition of {query}",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return await event.delete()
    else:
        return await event.edit(result)



# kanged from Blank-x ;---;
@register(outgoing=True, pattern=r"^\.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(" ")
        final_name = "+".join(remove_space)
        page = get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=r" +
            final_name +
            "&s=all")
        soup = BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = ("http://www.imdb.com/" +
                    odds[0].findNext("td").findNext("td").a["href"])
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, "lxml")
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        credits = soup.findAll("div", "credit_summary_item")
        director = credits[0].a.text
        if len(credits) == 1:
            writer = "Not available"
            stars = "Not available"
        elif len(credits) > 2:
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            writer = "Not available"
            actors = []
            for x in credits[1].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find(
                "div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        await e.edit(
            "<a href=" + poster + ">&#8203;</a>"
            "<b>Title : </b><code>"
            + mov_title
            + "</code>\n<code>"
            + mov_details
            + "</code>\n<b>Rating : </b><code>"
            + mov_rating
            + "</code>\n<b>Country : </b><code>"
            + mov_country[0]
            + "</code>\n<b>Language : </b><code>"
            + mov_language[0]
            + "</code>\n<b>Director : </b><code>"
            + director
            + "</code>\n<b>Writer : </b><code>"
            + writer
            + "</code>\n<b>Stars : </b><code>"
            + stars
            + "</code>\n<b>IMDB Url : </b>"
            + mov_link
            + "\n<b>Story Line : </b>"
            + story_line,
            link_preview=True,
            parse_mode="HTML",
        )
    except IndexError:
        await e.edit("Plox enter **Valid movie name** kthx")



        
@register(pattern=r"\.lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            return await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`"
            )
    elif util == "tts":
        scraper = "Text to Speech"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            return await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TTS`:\n\n`{tts_langs()}`"
            )
    await value.edit(f"`Language for {scraper} changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for {scraper} changed to {LANG.title()}.`"
        )

@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    detector = tr()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply to a message to translate!`")
        return
    try:
        reply_text = await detector.translate(deEmojify(message),
                                          targetlang=TRT_LANG)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    try:
        source_lan = await detector.detect(deEmojify(message))
        source_lan = LANGUAGES.get(source_lan).title()
        
    except:
        source_lan = "(Google didn't provide this info.)"

    reply_text = f"From: **{source_lan}**\nTo: **{LANGUAGES.get(TRT_LANG).title()}**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translated some {source_lan.title()} stuff to {LANGUAGES[TRT_LANG].title()} just now.",
        )
@register(outgoing=True, pattern=r"^\.yt(?: |$)(\d*)? ?(.*)")
async def yt_search(event):
    """ For .yt command, do a YouTube search from Telegram. """

    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))

    if not query:
        return await event.edit("`Reply to a message or pass a query to search!`")

    await event.edit("`Processing...`")

    if event.pattern_match.group(1) != "":
        counter = int(event.pattern_match.group(1))
        if counter > 10:
            counter = int(10)
        if counter <= 0:
            counter = int(1)
    else:
        counter = int(3)

    try:
        results = json.loads(
            YoutubeSearch(
                query,
                max_results=counter).to_json())
    except KeyError:
        return await event.edit(
            "`Youtube Search gone retard.\nCan't search this query!`"
        )

    output = f"**Search Query:**\n`{query}`\n\n**Results:**\n"

    for i in results["videos"]:
        try:
            title = i["title"]
            link = "https://youtube.com" + i["url_suffix"]
            channel = i["channel"]
            duration = i["duration"]
            views = i["views"]
            output += f"[{title}]({link})\nChannel: `{channel}`\nDuration: {duration} | {views}\n\n"
        except IndexError:
            break

    await event.edit(output, link_preview=False)


def deEmojify(inputString):
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


CMD_HELP.update(
    {
        "img": ">`.img [count] <query> [or reply]`"
        "\nUsage: Does an image search on DuckDuckGo.",
        "currency": ">`.currency <amount> <from> <to>`"
        "\nUsage: Converts various currencies for you.",
        "ipinfo": ">`.ipinfo <ip_address>`"
        "\nUsage: Gets the info of given ipaddress, send .ipinfo for bot's server ip info",
        "carbon": ">`.carbon <text> [or reply]`"
        "\nUsage: Beautify your code using carbon.now.sh\n"
        "Use .crblang <text> to set language for your code.",
        "duckduckgo": ">`.ddg <query> [or reply]`"
        "\nUsage: Does a search on DuckDuckGo.",
        "wiki": ">`.wiki <query> [or reply]`"
        "\nUsage: Does a search on Wikipedia.",
        "ud": ">`.ud <query> [or reply]`"
        "\nUsage: Does a search on Urban Dictionary.",
        "tts": ">`.tts <text> [or reply]`"
        "\nUsage: Translates text to speech for the language which is set."
        "\nUse >`.lang tts <language code>` to set language for tts. (Default is English.)",
        "trt": ">`.trt <text> [or reply]`"
        "\nUsage: Translates text to the language which is set."
        "\nUse >`.lang trt <language code>` to set language for trt. (Default is English),  you can also set environment variable for this, TRT_LANG and then the language code",
        "imdb": ">`.imdb <movie-name>`"
        "\nUsage: Shows movie info and other stuff.",
    })
