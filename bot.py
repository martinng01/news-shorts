import telebot
import os
from dotenv import load_dotenv

load_dotenv("./.env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
CHAT_ID = -1001998376109


def send_video(video_path: str, link, title: str = "", desc: str = ""):
    caption = ""
    if desc != "":
        caption = (f"*{title}*\n"
                   f"\n"
                   f"{desc}\n"
                   f"\n"
                   f"{link}")
    else:
        caption = (f"*{title}*\n"
                   f"\n"
                   f"{link}")

    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    bot.send_video(CHAT_ID,
                   video=open(video_path, "rb"),
                   parse_mode='Markdown',
                   caption=caption,
                   disable_notification=True,
                   timeout=200)
