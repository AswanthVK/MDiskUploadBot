import os
import string
import asyncio
from mdisky import Mdisk
from pyrogram import Client, filters


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

API_KEY = os.environ.get("API_KEY", "ox1G5YFFLX0uBxLee7Mn")


mdisk = Mdisk(API_KEY)

app = Client("tgid", bot_token=BOT_TOKEN, api_hash=API_HASH, api_id=API_ID)


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋", reply_to_message_id=message.message_id)


@app.on_message(filters.command(['mdisk']))
async def mdisk(client, message):
    await client.send_chat_action(message.chat.id, "typing")

    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    link = await mdisk.convert(url)
    await message.reply_text(text=f"{link}")
    print(link)


@app.on_message(filters.command(['rename']))
async def rename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    #link = "https://mdisk.me/convertor/16x9/5JIit7"
    link = await mdisk.change_filename(url, '@NewBotz')
    await message.reply_text(text=f"**New Filename:** {link}\n\n**URL:** {url}")
    print(link)


app.run()
