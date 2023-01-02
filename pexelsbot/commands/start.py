from pexelsbot import application
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode
from html import escape


START_TEXT = """
Hey there, <b>{}</b>.
I can fetch image or video from <a href='https://pexels.com'>Pexels</a> for you.

I use <a href="https://pexels.com/api/documentation">Pexels API</a> and \
<a href="https://pypi.org/project/python-pexels.com">python-pexels</a> library to get media.

Disclaimer: All images/videos are subject to copyright, you should give credits to the creator \
while using the image/video fetched from <a href='https://pexels.com'>Pexels</a>.
"""

START_KEYBOARD = [
    [
        InlineKeyboardButton(
            text="Image",
            callback_data="start_image"
        ),
        InlineKeyboardButton(
            text="Video",
            callback_data="start_video"
        )
    ],
    [
        InlineKeyboardButton(
            text="Creator",
            url="tg://user?id=2094704420`"
        ),
        InlineKeyboardButton(
            text="Source Code",
            url="https://github.com/Black-Bulls-Bots"
        )
    ]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    await message.reply_text(
        START_TEXT.format(escape(user.first_name)), 
        parse_mode=ParseMode.HTML, 
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )

async def start_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = update.effective_message
    user = update.effective_user
    data = query.data.split("_")
    print(data)
    if data[1] == "back":
        await message.edit_text(
            START_TEXT.format(escape(user.first_name)), 
        parse_mode=ParseMode.HTML, 
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
        )
    
    elif data[1] == "image":
        await message.edit_text(
            f"Images",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Back", callback_data="start_back")
                ]]
            )
        )
    elif data[1] == "video":
        await message.edit_text(
            f"Videos",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Back", callback_data="start_back")
                ]]
            )
        )


START_HANDLER = CommandHandler("start", start, block=False)
START_BUTTON_HANDLER = CallbackQueryHandler(start_buttons, pattern="start_", block=False)

application.add_handler(START_HANDLER)
application.add_handler(START_BUTTON_HANDLER)
