import asyncio

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from tools.googles import google_search
from tools.helpers import Parameters


@Client.on_message(command("google"))
async def google(_: Client, msg: Message):
    """谷歌搜索，并展示前9条标题记录"""
    replied_msg = msg.reply_to_message
    if not replied_msg:
        _, args = Parameters.get(msg)
    else:
        args = replied_msg.text or replied_msg.caption

    try:
        res = await google_search(args)
        content = '\n\n'.join(
            f"[{k}]({v})" for k, v in res.items()
        )
        text = f"🔎 | **Google** | `{args}`\n{content}"
        await msg.edit_text(
            text=text,
            parse_mode='md',
            disable_web_page_preview=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await msg.edit_text(
            text=text,
            parse_mode='md',
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(e)
        await msg.edit_text("❗️ Unable to connect to google")
    finally:
        await logger.complete()
