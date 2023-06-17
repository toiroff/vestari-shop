import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton,ReplyKeyboardMarkup
from loader import db


async def products_keyboard():
    g =db.select_menu()
    for i in g:
        raqam = int(f"{i[1]}")
        markup = InlineKeyboardMarkup(row_width=raqam)
    products = db.select_all_product()
    for product in products:
        button_text = f"{product[1]}"
        callback_data = f"mahsulot:{product[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup

async def category_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    ctg = db.get_category()
    for c in ctg:
        button_text = f"{c[1]}"
        callback_data = f"{c[1:]}"
        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=f"category:{button_text}"))

    markup.insert(InlineKeyboardButton(text="◀️ Back",callback_data='product_back'))
    return markup

async def select_category_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    ctg = db.get_category()
    for c in ctg:
        button_text = f"{c[1]}"
        callback_data = f"{c[1:]}"
        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=f"category:{button_text}"))


    return markup


async def buy_keyboard(product_id):
    markup = InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text="📦 Make an order",callback_data=f"get:{product_id}"),
                InlineKeyboardButton(text="◀️Back",callback_data="orqaga"))
    return markup

async def numberorder(id,volume=None):
    # max_count = db.count_order(volume)
    markup = InlineKeyboardMarkup(row_width=3).add(
                InlineKeyboardButton(text="➖",callback_data=f"minus:{id}:{volume}"),
                InlineKeyboardButton(text=f"{volume}",callback_data=f"volume"),
                InlineKeyboardButton(text="➕",callback_data=f"plus:{id}:{volume}"),
                InlineKeyboardButton(text="◀️Back", callback_data=f"Orqaga:{id}"),
                InlineKeyboardButton(text="🛒 Add to basket", callback_data=f"savat:{id}:{volume}"))
    return markup

async def check_of_order(order_id):
    markup = InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="➕ Add product",callback_data="add"),
                InlineKeyboardButton(text="✅ Order confirmation", callback_data=f"tasdiq"),
                InlineKeyboardButton(text="🗑 Cleaning the basket",callback_data=f"delete"),
                InlineKeyboardButton(text="◀ Back",callback_data=f"somet:{order_id}"))

    return markup

yes_no = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "✅ YES", callback_data = "XA"),
            InlineKeyboardButton(text = "❌ NO", callback_data = "YOQ")
        ]
    ]
)

async def acceptance(user_id, order_id):
    markup =InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="✅ Acceptance",callback_data=f"accept:{user_id}:{order_id}"),
                InlineKeyboardButton(text="❌ Refusal",callback_data=f"reject:{user_id}:{order_id}"))
    return markup

async def buttons_for_basket():
    markup = InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text="✅ Order confirmation", callback_data=f"tasdiq"),
                InlineKeyboardButton(text="🗑 Clear the basket",callback_data=f"delete"))
    return markup