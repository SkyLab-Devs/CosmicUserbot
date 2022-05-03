# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.

""" Userbot module containing commands related to android. """

import asyncio
import json
import math
import os
import re
import time

from bs4 import BeautifulSoup
from requests import get

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import chrome, human_to_bytes, humanbytes, md5, time_formatter

GITHUB = "https://github.com"


@register(outgoing=True, pattern=r"^\.magisk$")
async def magisk(request):
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/beta.json",
        "Canary": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/canary.json",
    }
    releases = "Latest Magisk Releases:\n"
    for name, release_url in magisk_dict.items():
        data = data = get(release_url).json()
        releases += (
            f'{name}: [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[Changelog]({data["magisk"]["note"]})\n'
        )
    await request.edit(releases)


@register(outgoing=True, pattern=r"^.device(?: |$)(\S*)")
async def device_info(request):
    """ get android device basic info from its codename """
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await request.edit("`Usage: .device <codename> / <model>`")
        return
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^.codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """ search for android codename """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .codename <brand> <device>`")
        return

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}  # Lower brand names in JSON
    devices = devices_lower.get(brand)
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Device**: {item['device']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern="^.pixeldl(?: |$)(.*)")
async def download_api(dl):
    await dl.edit("`Collecting information...`")
    URL = dl.pattern_match.group(1)
    URL_MSG = await dl.get_reply_message()
    if URL:
        pass
    elif URL_MSG:
        URL = URL_MSG.text
    else:
        await dl.edit("`Empty information...`")
        return
    if not re.findall(r"\bhttps?://download.*pixelexperience.*\.org\S+", URL):
        await dl.edit("`Invalid information...`")
        return
    driver = await chrome()
    await dl.edit("`Getting information...`")
    driver.get(URL)
    error = driver.find_elements_by_class_name("swal2-content")
    if len(error) > 0:
        if error[0].text == "File Not Found.":
            await dl.edit(f"`FileNotFoundError`: {URL} is not found.")
            return
    datas = driver.find_elements_by_class_name("download__meta")
    """ - enumerate data to make sure we download the matched version - """
    md5_origin = None
    i = None
    for index, value in enumerate(datas):
        for data in value.text.split("\n"):
            if data.startswith("MD5"):
                md5_origin = data.split(":")[1].strip()
                i = index
                break
        if md5_origin is not None and i is not None:
            break
    if md5_origin is None and i is None:
        await dl.edit("`There is no match version available...`")
    if URL.endswith("/"):
        file_name = URL.split("/")[-2]
    else:
        file_name = URL.split("/")[-1]
    file_path = TEMP_DOWNLOAD_DIRECTORY + file_name
    download = driver.find_elements_by_class_name("download__btn")[i]
    download.click()
    await dl.edit("`Starting download...`")
    file_size = human_to_bytes(download.text.split(None, 3)[-1].strip("()"))
    display_message = None
    complete = False
    start = time.time()
    while complete is False:
        if os.path.isfile(file_path + ".crdownload"):
            try:
                downloaded = os.stat(file_path + ".crdownload").st_size
                status = "Downloading"
            except OSError:  # Rare case
                await asyncio.sleep(1)
                continue
        elif os.path.isfile(file_path):
            downloaded = os.stat(file_path).st_size
            file_size = downloaded
            status = "Checking"
        else:
            await asyncio.sleep(0.3)
            continue
        diff = time.time() - start
        percentage = downloaded / file_size * 100
        speed = round(downloaded / diff, 2)
        eta = round((file_size - downloaded) / speed)
        prog_str = "`{0}` | [{1}{2}] `{3}%`".format(
            status,
            "".join(["■" for i in range(math.floor(percentage / 10))]),
            "".join(["▨" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        current_message = (
            "`[DOWNLOAD]`\n\n"
            f"`{file_name}`\n"
            f"`Status`\n{prog_str}\n"
            f"`{humanbytes(downloaded)} of {humanbytes(file_size)}"
            f" @ {humanbytes(speed)}`\n"
            f"`ETA` -> {time_formatter(eta)}"
        )
        if (
            round(diff % 15.00) == 0
            and display_message != current_message
            or (downloaded == file_size)
        ):
            await dl.edit(current_message)
            display_message = current_message
        if downloaded == file_size:
            if not os.path.isfile(file_path):  # Rare case
                await asyncio.sleep(1)
                continue
            MD5 = await md5(file_path)
            if md5_origin == MD5:
                complete = True
            else:
                await dl.edit("`Download corrupt...`")
                os.remove(file_path)
                driver.quit()
                return
    await dl.respond(f"`{file_name}`\n\n" f"Successfully downloaded to `{file_path}`.")
    await dl.delete()
    driver.quit()
    return


@register(outgoing=True, pattern=r"^.specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """ Mobile devices specifications """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .specs <brand> <device>`")
        return
    
    gsm = get(f"https://api-mobilespecs.azharimm.site/v2/search?query={brand} {device}").json()
    devs = gsm['data']['phones']
    res = len(devs)
    i = 0

    while i < res:
        phonename = devs[i]['phone_name'].replace("(","").replace(")","") #replace ( and ) in phone names
        chk = all(elem in phonename.lower().split(" ") for elem in device.lower().split(" "))
        if chk and devs[i]['brand'].lower() == brand.lower():
                phun = i
        i += 1
    try:
        check = devs[phun]['phone_name']
    except:
        await request.edit("```Prolly phone doesnt exist... Try googling?```")
        return()

    specreq = get(devs[phun]['detail']).json()
    specsjson = specreq["data"]["specifications"]

    img = specreq["data"]["phone_images"][0]
    out = ""
    out += "**" + specreq["data"]["brand"] + " " + specreq["data"]["phone_name"] + "**\n"
    out += f"• Device Image: [Here]({img}) \n"
    for spec in specsjson:
        title = spec["title"]
        title = title.rstrip()
        out += f'\n**{title}**\n'
        for val in spec["specs"]:
            featvalue = ''.join(map(str, val['val']))
            featvalue = featvalue.replace("\n","")
            out += f"• {val['key']} : {featvalue} \n"

    await request.edit(out)
@register(outgoing=True, pattern=r"^.twrp(?: |$)(\S*)")
async def twrp(request):
    """ get android device twrp """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("`Usage: .twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)

@register(outgoing=True, pattern=r"^.ofox(?: |$)(\S*)")
async def ofox(request):
    """ get android device ofox """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("`Usage: .ofox <codename>`")
        return
    url = get(f"https://api.orangefox.download/v3/devices/get?codename={device}")
    if url.status_code == 404:
        await request.edit(f"`Couldn't find OrangeFox Recovery for {device}!`\n")
        return
    info = json.loads(url.text)
    if 'url' in info:
        ed = (
          f"**Latest OFOX Recovery for {info['full_name']}:**\n"
          f"[{device}]({info['url']})\n"
          f"Maintainer: {info['maintainer']['name']}"
           )
        await request.edit(ed)
    else:
        await request.edit("Mmmm... Some issue occured")

CMD_HELP.update(
    {
        "android": ".magisk\
\nGet latest Magisk releases\
\n\n.device <codename>\
\nUsage: Get info about android device codename or model.\
\n\n.codename <brand> <device>\
\nUsage: Search for android device codename.\
\n\n.pixeldl **<download.pixelexperience.org>**\
\nUsage: Download pixel experience ROM into your userbot server.\
\n\n.specs <brand> <device>\
\nUsage: Get device specifications info from GSMArena.\
\n\n.twrp <codename>\
\nUsage: Get latest twrp download for android device.\
\n\n.ofox <codename>\
\nUsage: Ger latest ofox recovery download for android device."
    }
)
