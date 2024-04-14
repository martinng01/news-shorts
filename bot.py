import telebot
import os
from dotenv import load_dotenv

load_dotenv("./.env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
CHAT_ID = -1001998376109


def send_video(video_path: str):
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    bot.send_video(CHAT_ID, video=open(video_path, "rb"), timeout=200)
