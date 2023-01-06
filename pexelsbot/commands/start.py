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

Please find the below buttons to get help.

<i>Disclaimer: All images/videos are subject to copyright, you should give credits to the creator \
while using the image/video fetched from <a href='https://pexels.com'>Pexels</a>.</i>
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
            url="tg://user?id=2094704420"
        ),
        InlineKeyboardButton(
            text="Source Code",
            url="https://github.com/Black-Bulls-Bots/pexelsbot"
        )
    ]
]

IMAGE_HELP = """
Hey there, you can search images using the command <code>/image</code>, please read more for \
further details.

You can just use <code>/image</code> to see what happens, or you can ask what you want using \
<code>/image search_term</code> and you can even ask how many results you want to fetch from the bot.

Examples:
1. <code>/image</code>
2. <code>/image nature</code>
3. <code>/image sunrise 12</code>

Caution:
You can't get results more than 80 at a time, so be cautious with the result limit.
By default bot returns 10 results
"""


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
            IMAGE_HELP,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Back", callback_data="start_back")
                ]]
            ),
            parse_mode=ParseMode.HTML,
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
    await query.answer()


START_HANDLER = CommandHandler("start", start, block=False)
START_BUTTON_HANDLER = CallbackQueryHandler(start_buttons, pattern="start_", block=False)

application.add_handler(START_HANDLER)
application.add_handler(START_BUTTON_HANDLER)
