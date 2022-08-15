import os
import string
import asyncio
import requests
from mdisk import Mdisk as MDisk
from mdisky import Mdisk
from database.database import *
from pyrogram import Client, filters


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

APP_ID = int(os.environ.get("APP_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

#API_KEY = os.environ.get("API_KEY", "")

app = Client("tgid", bot_token=TG_BOT_TOKEN, api_hash=API_HASH, api_id=APP_ID)


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋\n\nI'm a telegram bot which convert MDisk link to your Link", reply_to_message_id=message.message_id)


@app.on_message(filters.command(['mdisk']))
async def mdisk(client, message):
    await client.send_chat_action(message.chat.id, "typing")
    a = await client.send_message(
            chat_id=message.chat.id,
            text=f"Processing…",
            reply_to_message_id=message.message_id
        )
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    if not url.startswith("https:"):
        return await message.reply_text(f"**INVALID LINK**", reply_to_message_id=message.message_id)    
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    d = MDisk(API_KEY)
    link = d.upload(url)
    await message.reply_text(text=f"{link}")
    await a.delete()
    print(link)


@app.on_message(filters.command(['convert']))
async def mdisk(client, message):
    await client.send_chat_action(message.chat.id, "typing")
    
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    link = await mdisk.convert(url)
    await message.reply_text(text=f"{link}")
    print(link)


@app.on_message(filters.command(['rename']))
async def rename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, txt = message.text.split(" ", 1)
    if ("|" in txt):
        url_parts = txt.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    link = await mdisk.change_filename(url, file_name)
    await message.reply_text(text=f"**New Filename:** {file_name}\n\n**URL:** {url}")
    print(link)


@app.on_message(filters.command(['filename']))
async def filename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    filename = await mdisk.get_filename(url)
    await message.reply_text(text=f"**Filename:** {filename}")
    print(filename)


@app.on_message(filters.command(['auth']))
async def set_caption(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "Use this command to set your own Mdisk Api Key \n\nEg:- `/auth your mdisk key`", 
            quote = True
        )
    else:
        command, caption = message.text.split(' ', 1)
        await update_caption(message.from_user.id, caption)
        await message.reply_text(f"__Authorised Successfully__", quote=True)


@app.on_message(filters.command(['me']))
async def view_caption(client, message):
    if (message is not None):
        try:
            caption = await get_caption(message.from_user.id)
            caption_text = caption.caption
        except:
            caption_text = "Not Authorised" 
        await message.reply_text(
            f"API KEY: {caption_text}",
            quote = True
        )


@app.on_message(filters.command(['unauth']))
async def view_caption(client, message):
    if (message is not None):
        try:
            caption = await del_caption(message.from_user.id)
        except:
            caption_text = "Not Authorised me" 
        await message.reply_text(
            "Unauthorised successfully",
            quote = True
        )


app.run()
