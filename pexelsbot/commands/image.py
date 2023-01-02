from pexelsbot import application, pexels
from Pexels.types import Photo
from Pexels.errors import PexelsError
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

async def search_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    args = context.args

    if len(args) < 1:
        await message.delete()
        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton('Yes', callback_data="image_trending_yes"),
                InlineKeyboardButton('No', callback_data="image_trending_no")
            ]]
        )
        await message.reply_text(
            "You didn't give any search term to search for,\n<b>Do you wanna check the trending ones?</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=buttons,
            )
        return
    
    if args[-1].isnumeric:
        try:
            per_page = int(args[-1])
        except:
            per_page = 10
    else:
        per_page = 10

    query = ' '.join(args)
    try:
        search = pexels.search_photos(query, per_page=per_page)
    except PexelsError:
        await message.reply_text(
            "Something happened, please try again after some time.  \
            \nPossible reason can be you requested per page photos over 80, try to reduce it. \
            \nOr it can be of any bot side issue too."
            )
        return


    for photo in search.photos:
        if isinstance(photo, Photo):
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Size", callback_data=f"image_size_{photo.id}"),
                        InlineKeyboardButton("URL", url=photo.url)
                    ],
                    [
                       InlineKeyboardButton("Photographer", url=photo.photographer_url)
                    ],
                ]
            )

            await context.bot.send_photo(
                update.effective_chat.id,
                photo.src.medium,
                caption=f'<i>{photo.alt}</i>',
                parse_mode=ParseMode.HTML,
                reply_markup=buttons,
            )
    await message.reply_text(
        f"Found <code>{search.total_results}</code> result(s)\nCurrent Page <code>{search.page}</code>", 
        parse_mode=ParseMode.HTML
        )
        
async def image_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = update.effective_message
    data = query.data.split("_")

    if len(data) >= 2:
        if data[1] == "size":
            photo = pexels.get_photo(data[2])
            buttons = [
                [
                        InlineKeyboardButton("Large", callback_data=f"image_large_{photo.id}"),
                        InlineKeyboardButton("Original", callback_data=f"image_original_{photo.id}"),
                    ],
                    [
                        InlineKeyboardButton("Portrait", callback_data=f"image_portrait_{photo.id}"),
                        InlineKeyboardButton("Landscape", callback_data=f"image_landscape_{photo.id}"),
                    ],
                    [
                        InlineKeyboardButton("Medium", callback_data=f"image_medium_{photo.id}"),
                        InlineKeyboardButton("Tiny", callback_data=f"image_tiny_{photo.id}"),
                    ],
                    [
                        InlineKeyboardButton("Back", callback_data=f"image_back_{photo.id}")
                    ]
            ]
            await message.edit_reply_markup(InlineKeyboardMarkup(buttons))
        elif data[1] == "back":
            photo = pexels.get_photo(data[2])
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Size", callback_data=f"image_size_{photo.id}"),
                        InlineKeyboardButton("URL", url=photo.url)
                    ],
                    [
                       InlineKeyboardButton("Photographer", url=photo.photographer_url)
                    ],
                ]
            )
            await message.edit_reply_markup(buttons)
        elif data[1] == "trending":
            if data[2] == "yes":
                search = pexels.search_curated_photo()

                for photo in search.photos:
                    if isinstance(photo, Photo):
                        buttons = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Size", callback_data=f"image_size_{photo.id}"),
                                    InlineKeyboardButton("URL", url=photo.url)
                                ],
                                [
                                InlineKeyboardButton("Photographer", url=photo.photographer_url)
                                ],
                            ]
                        )

                        await context.bot.send_photo(
                            update.effective_chat.id,
                            photo.src.medium,
                            caption=f'<i>{photo.alt}</i>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=buttons,
                        )
            elif data[2] == "no":
                await query.answer("Umm, try again with some search term or get trending ones.", show_alert=True)
                await message.delete()
                return
        else:
            photo = pexels.get_photo(data[2])
            if hasattr(photo.src, data[1]):
                await context.bot.send_document(
                    update.effective_chat.id,
                    getattr(photo.src, data[1]),
                    caption=f'<i>{photo.alt}</i>',
                    parse_mode=ParseMode.HTML,
                )
        await query.answer()

IMAGE_HANDLER = CommandHandler("image", search_photo, block=False)
IMAGE_BUTTONS = CallbackQueryHandler(image_buttons, "image_")

application.add_handler(IMAGE_HANDLER)
application.add_handler(IMAGE_BUTTONS)