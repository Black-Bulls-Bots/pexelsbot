"""
Pexels Bot for Telegram
Which can fetch free stock videos or images from Pexels API.
Images/Videos are subject to copyright, so better use them with giving credits.

Author: Kishore
Email: jokerhacker.6521@protonmail.com
Telegram: https://t.me/Kishoreee
"""

import os
import logging
from dotenv import load_dotenv
from Pexels import Client
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton

#setup logger config to our needs, change level as you want.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.DEBUG,
)

#load env variables from .env files.
load_dotenv()

LOGGER = logging.getLogger(__name__)

#get bot token from env variable stored in .env file.
BOT_TOKEN = os.getenv("BOT_TOKEN")

PEXELS_TOKEN = os.getenv("PEXELS_TOKEN")

if BOT_TOKEN is None:
    LOGGER.info("Bot TOKEN is missing, check your env.")
    exit()

if PEXELS_TOKEN is None:
    LOGGER.info("Pexels API TOKEN is missing, check your env.")
    exit()

#build application from bot token.
application = ApplicationBuilder().token(BOT_TOKEN).build()

pexels = Client(PEXELS_TOKEN)
