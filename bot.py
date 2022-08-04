import os
import string
import asyncio
import requests
from mdisky import Mdisk
from pyrogram import Client, filters


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

API_KEY = os.environ.get("API_KEY", "ox1G5YFFLX0uBxLee7Mn")

app = Client("tgid", bot_token=BOT_TOKEN, api_hash=API_HASH, api_id=API_ID)


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋", reply_to_message_id=message.message_id)


@app.on_message(filters.regex('http') & filters.private)
async def mdisk(client, message):
    await client.send_chat_action(message.chat.id, "typing")

    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    if ("|" in url):
        url_parts = url.split("|")
        if len(url_parts) == 2:
            dl_url = url_parts[0]
            file_name = url_parts[1]
    else:
        dl_url = url
    mdisk = Mdisk(API_KEY)
    link = await mdisk.convert(dl_url)
    link0 = await mdisk.change_filename(dl_url, file_name)
    await message.reply_text(text=f"{dl_url}")
    print(link)


@app.on_message(filters.command(['rename']))
async def rename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    mdisk = Mdisk(API_KEY)
    link = await mdisk.change_filename(url, '@NewBotz')
    await message.reply_text(text=f"**New Filename:** {link}\n\n**URL:** {url}")
    print(link)


@app.on_message(filters.command(['filename']))
async def filename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    mdisk = Mdisk(API_KEY)
    filename = await mdisk.get_filename(url)
    await message.reply_text(text=f"**Filename:** {filename}")
    print(filename)


app.run()
