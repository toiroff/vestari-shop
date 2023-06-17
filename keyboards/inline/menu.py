from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

DATAS = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "📝 Edit information", callback_data="editdata"),
        ],
        [
            InlineKeyboardButton(text = "◀️ Back", callback_data="back_settings"),
        ]
    ],
    row_width=1
)


EDITDATAS = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "📝 Edit your name", callback_data="edit_name"),
        ],
        [
            InlineKeyboardButton(text = "📝 Edit your phone number", callback_data="edit_phone"),
        ],
        [
            InlineKeyboardButton(text = "◀️ Back", callback_data="back_settings"),
        ]
    ],
    row_width=1
)

async def messages():
    # g =db.select_menu()
    # for i in g:
    #     raqam = int(f"{i[1]}")
    markup = InlineKeyboardMarkup(row_width=1)
    products= db.select_all_tarmoq()
    for x in products:
        button_text = x[1]
        callback_data = f"{x[2]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,url=callback_data)
                      )
    return markup



