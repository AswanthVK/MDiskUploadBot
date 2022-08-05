import os
import string
import asyncio
from mdisky import Mdisk
from database.database import *
from pyrogram import Client, filters


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

API_KEY = os.environ.get("API_KEY", "ox1G5YFFLX0uBxLee7Mn")

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
    mdisk = Mdisk(API_KEY)
    link = await mdisk.convert(url)
    #link0 = await mdisk.change_filename(url, file_name)
    await message.reply_text(text=f"{link}")
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


@app.on_message(filters.command(['set_caption']))
async def set_caption(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "🖊️ 𝐒𝐄𝐓 𝐂𝐀𝐏𝐓𝐈𝐎𝐍 \n\nUse this command to set your own caption text \n\n👉 `set_caption My Caption`", 
            quote = True
        )
    else:
        command, caption = message.text.split(' ', 1)
        await update_caption(message.from_user.id, caption)
        await message.reply_text(f"**--Your Caption--:**\n\n{caption}", quote=True)


@app.on_message(filters.command(['view_caption']))
async def view_caption(client, message):
    if (message is not None):
        try:
            caption = await get_caption(message.from_user.id)
            caption_text = caption.caption
        except:
            caption_text = "Not Added" 
        await message.reply_text(
            text=f"**--Your Caption--**\n\n{caption_text}",
            parse_mode="html", 
            disable_web_page_preview=True
        )


app.run()
