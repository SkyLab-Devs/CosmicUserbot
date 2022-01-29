# Copyright (C) 2019 The Raphielscape Company LLC.; Licensed under the Raphielscape Public License, Version 1.d (the "License"); you may not use this file except in compliance with the License.; The entire source code is OSSRPL except; 'download, uploadir, uploadas, upload' which is MPL; License: MPL and OSSRPL

""" Userbot module which contains everything related to downloading/uploading from/to the server. """

import asyncio
import math
import os
import time
from datetime import datetime
from urllib.parse import unquote_plus

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pySmartDL import SmartDL
from requests import get
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo

from userbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import humanbytes, progress, run_cmd
from userbot.utils.FastTelethon import download_file, upload_file


@register(pattern=r"\.dl(?: |$)(.*)", outgoing=True)
async def download(target_file):
    """ For .download command, download files to the userbot's server. """
    await target_file.edit("**Processing...**")
    input_str = target_file.pattern_match.group(1)
    replied = await target_file.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if input_str:
        url = input_str
        file_name = unquote_plus(os.path.basename(url))
        if "|" in input_str:
            url, file_name = input_str.split("|")
            url = url.strip()
            # https://stackoverflow.com/a/761825/4723940
            file_name = file_name.strip()
            head, tail = os.path.split(file_name)
            if head:
                if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                    os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                    file_name = os.path.join(head, tail)
        try:
            url = get(url).url
        except BaseException:
            return await target_file.edit("**This is not a valid link.**")
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            progress_str = "[{}{}] `{}%`".format(
                "".join("■" for _ in range(math.floor(percentage / 10))),
                "".join("▨" for _ in range(10 - math.floor(percentage / 10))),
                round(percentage, 2),
            )

            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = (
                    f"**Name:** `{file_name}`\n"
                    f"\n**{status}...** | {progress_str}"
                    f"\n{humanbytes(downloaded)} of {humanbytes(total_length)}"
                    f" @ {humanbytes(speed)}"
                    f"\n**ETA:** {estimated_total_time}"
                )

                if round(diff % 15.00) == 0 and current_message != display_message:
                    await target_file.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
        if downloader.isSuccessful():
            await target_file.edit(
                f"**Downloaded to** `{downloaded_file_name}` **successfully!**"
            )
        else:
            await target_file.edit(f"**Incorrect URL**\n{url}")
    elif replied:
        if not replied.media:
            return await target_file.edit("**Reply to file or media.**")
        try:
            media = replied.media
            if hasattr(media, "document"):
                file = media.document
                mime_type = file.mime_type
                filename = replied.file.name
                if not filename:
                    if "audio" in mime_type:
                        filename = (
                            "audio_" + datetime.now().isoformat("_", "seconds") + ".ogg"
                        )
                    elif "video" in mime_type:
                        filename = (
                            "video_" + datetime.now().isoformat("_", "seconds") + ".mp4"
                        )
                outdir = TEMP_DOWNLOAD_DIRECTORY + filename
                c_time = time.time()
                start_time = datetime.now()
                with open(outdir, "wb") as f:
                    result = await download_file(
                        client=target_file.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                target_file,
                                c_time,
                                "Telegram - Download",
                                input_str,
                            )
                        ),
                    )
            else:
                start_time = datetime.now()
                result = await target_file.client.download_media(
                    media, TEMP_DOWNLOAD_DIRECTORY
                )
            dl_time = (datetime.now() - start_time).seconds
        except Exception as e:  # pylint:disable=C0103,W0703
            await target_file.edit(str(e))
        else:
            try:
                await target_file.edit(
                    f"**Downloaded to** `{result.name}` **in {dl_time} seconds.**"
                )
            except AttributeError:
                await target_file.edit(
                    f"**Downloaded to** `{result}` **in {dl_time} seconds.**"
                )
    else:
        await target_file.edit("**See** `.help download` **for more info.**")


async def get_video_thumb(file, output):
    """ Get video thumbnail """
    command = ["ffmpeg", "-i", file, "-ss", "00:00:01.000", "-vframes", "1", output]
    t_resp, e_resp = await run_cmd(command)
    if os.path.lexists(output):
        return output
    LOGS.info(t_resp)
    LOGS.info(e_resp)
    return None


@register(pattern=r"^\.ul (.*)", outgoing=True)
async def upload(event):
    await event.edit("**Processing...**")
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        if os.path.isfile(input_str):
            c_time = time.time()
            start_time = datetime.now()
            file_name = os.path.basename(input_str)
            thumb = None
            attributes = []
            with open(input_str, "rb") as f:
                result = await upload_file(
                    client=event.client,
                    file=f,
                    name=file_name,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, c_time, "Telegram - Upload", input_str)
                    ),
                )
            up_time = (datetime.now() - start_time).seconds
            if input_str.lower().endswith(("mp4", "mkv", "webm")):
                thumb = await get_video_thumb(input_str, "thumb_image.jpg")
                metadata = extractMetadata(createParser(input_str))
                duration = 0
                width = 0
                height = 0
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                attributes = [
                    DocumentAttributeVideo(
                        duration=duration,
                        w=width,
                        h=height,
                        round_message=False,
                        supports_streaming=True,
                    )
                ]
            elif input_str.lower().endswith(("mp3", "flac", "wav")):
                metadata = extractMetadata(createParser(input_str))
                duration = 0
                artist = ""
                title = ""
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
                if metadata.has("title"):
                    title = metadata.get("title")
                if metadata.has("artist"):
                    artist = metadata.get("artist")
                attributes = [
                    DocumentAttributeAudio(
                        duration=duration,
                        title=title,
                        performer=artist,
                    )
                ]
            await event.client.send_file(
                event.chat_id,
                result,
                thumb=thumb,
                caption=file_name,
                force_document=False,
                allow_cache=False,
                reply_to=event.message.id,
                attributes=attributes,
            )
            if thumb is not None:
                os.remove(thumb)
            await event.edit(f"**Uploaded successfully in {up_time} seconds.**")
        elif os.path.isdir(input_str):
            start_time = datetime.now()
            lst_files = []
            for root, _, files in os.walk(input_str):
                for file in files:
                    lst_files.append(os.path.join(root, file))
            if not lst_files:
                return await event.edit(f"`{input_str}` **is empty.**")
            await event.edit(f"**Found** `{len(lst_files)}` **files. Uploading...**")
            for files in sorted(lst_files):
                file_name = os.path.basename(files)
                thumb = None
                attributes = []
                msg = await event.reply(f"**Uploading** `{files}`**...**")
                with open(files, "rb") as f:
                    result = await upload_file(
                        client=event.client,
                        file=f,
                        name=file_name,
                    )
                if file_name.lower().endswith(("mp4", "mkv", "webm")):
                    thumb = await get_video_thumb(files, "thumb_image.jpg")
                    metadata = extractMetadata(createParser(files))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                elif file_name.lower().endswith(("mp3", "flac", "wav")):
                    metadata = extractMetadata(createParser(files))
                    duration = 0
                    title = ""
                    artist = ""
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("title"):
                        title = metadata.get("title")
                    if metadata.has("artist"):
                        artist = metadata.get("artist")
                    attributes = [
                        DocumentAttributeAudio(
                            duration=duration,
                            title=title,
                            performer=artist,
                        )
                    ]
                await event.client.send_file(
                    event.chat_id,
                    result,
                    thumb=thumb,
                    caption=file_name,
                    force_document=False,
                    allow_cache=False,
                    attributes=attributes,
                )
                await msg.delete()
                if thumb is not None:
                    os.remove(thumb)

            await event.delete()
            up_time = (datetime.now() - start_time).seconds
            await event.respond(
                f"**Uploaded {len(lst_files)} files in** `{input_str}` **folder "
                f"in {up_time} seconds.**"
            )
    else:
        await event.edit("**Error: File/Folder not found**")

@register(pattern=r".download(?: |$)(.*)", outgoing=True)
async def download(target_file):
    """ For .download command, download files to the userbot's server. """
    await target_file.edit("Processing ...")
    input_str = target_file.pattern_match.group(1)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if "|" in input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        head, tail = os.path.split(file_name)
        if head:
            if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                file_name = os.path.join(head, tail)
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "/" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            progress_str = "[{0}{1}] `{2}%`".format(
                "".join(["■" for i in range(math.floor(percentage / 10))]),
                "".join(["▨" for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2),
            )
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = (
                    f"`Name` : `{file_name}`\n"
                    "Status"
                    f"\n**{status}**... | {progress_str}"
                    f"\n{humanbytes(downloaded)} of {humanbytes(total_length)}"
                    f" @ {speed}"
                    f"\n`ETA` -> {estimated_total_time}"
                )

                if round(diff % 10.00) == 0 and current_message != display_message:
                    await target_file.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
        if downloader.isSuccessful():
            await target_file.edit(
                "Downloaded to `{}` successfully !!".format(downloaded_file_name)
            )
        else:
            await target_file.edit("Incorrect URL\n{}".format(url))
    elif target_file.reply_to_msg_id:
        try:
            c_time = time.time()
            downloaded_file_name = await target_file.client.download_media(
                await target_file.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, target_file, c_time, "[DOWNLOAD]")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await target_file.edit(str(e))
        else:
            await target_file.edit(
                "Downloaded to `{}` successfully !!".format(downloaded_file_name)
            )
    else:
        await target_file.edit("Reply to a message to download to my local server.")


@register(pattern=r".uploadir (.*)", outgoing=True)
async def uploadir(udir_event):
    """ For .uploadir command, allows you to upload everything from a folder in the server"""
    input_str = udir_event.pattern_match.group(1)
    if os.path.exists(input_str):
        await udir_event.edit("Processing ...")
        lst_of_files = []
        for r, d, f in os.walk(input_str):
            for file in f:
                lst_of_files.append(os.path.join(r, file))
            for file in d:
                lst_of_files.append(os.path.join(r, file))
        LOGS.info(lst_of_files)
        uploaded = 0
        await udir_event.edit(
            "Found {} files. Uploading will start soon. Please wait!".format(
                len(lst_of_files)
            )
        )
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, udir_event, c_time, "[UPLOAD]", single_file)
                        ),
                    )
                else:
                    thumb_image = os.path.join(input_str, "thumb.jpg")
                    c_time = time.time()
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        thumb=thumb_image,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, udir_event, c_time, "[UPLOAD]", single_file)
                        ),
                    )
                os.remove(single_file)
                uploaded = uploaded + 1
        await udir_event.edit("Uploaded {} files successfully !!".format(uploaded))
    else:
        await udir_event.edit("404: Directory Not Found")


@register(pattern=r".upload (.*)", outgoing=True)
async def upload(u_event):
    """ For .upload command, allows you to upload a file from the userbot's server """
    await u_event.edit("Processing ...")
    input_str = u_event.pattern_match.group(1)
    if input_str in ("userbot.session", "config.env"):
        return await u_event.edit("`That's a dangerous operation! Not Permitted!`")
    if os.path.exists(input_str):
        c_time = time.time()
        await u_event.client.send_file(
            u_event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=u_event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, u_event, c_time, "[UPLOAD]", input_str)
            ),
        )
        await u_event.edit("Uploaded successfully !!")
    else:
        await u_event.edit("404: File Not Found")



def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@register(pattern=r".uploadas(stream|vn|all) (.*)", outgoing=True)
async def uploadas(uas_event):
    """ For .uploadas command, allows you to specify some arguments for upload. """
    await uas_event.edit("Processing ...")
    type_of_upload = uas_event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    input_str = uas_event.pattern_match.group(2)
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb_path = "a_random_f_file_name" + ".jpg"
        thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "[UPLOAD]", file_name)
                    ),
                )
            elif round_message:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "[UPLOAD]", file_name)
                    ),
                )
            elif spam_big_messages:
                return await uas_event.edit("TBD: Not (yet) Implemented")
            os.remove(thumb)
            await uas_event.edit("Uploaded successfully !!")
        except FileNotFoundError as err:
            await uas_event.edit(str(err))
    else:
        await uas_event.edit("404: File Not Found")

CMD_HELP.update(
    {
        "download": ">`.download` <link> | <filename> (optional)"
        "\nUsage: Downloads file from url to the server."
        "\n\n>`.dl` <reply to file> Unstable but fast"
        "\n\n>`.download` <file path in server> Stable but slow" 
        "\nUsage: Downloads file from the replied file/media."
        "\n\n>`.ul` <file/folder path in server> Unstable but fast"
        "\n\n>`.upload <path in server>" 
        "\nUsage: Uploads a locally stored file/folder to the chat."
    }
)
