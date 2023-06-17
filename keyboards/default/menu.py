from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🛍 Products"),
        ],
        [
            KeyboardButton(text = "📄 My orders"),
            # KeyboardButton(text = "🔵 Biz ijtimoiy tarmoqlarda"),
        ],
        [
            KeyboardButton(text = "📞 Contact us"),
            KeyboardButton(text = "⚙️ Settings"),
        ],
        [
            KeyboardButton(text = "🛒 Basket")
        ]
    ],
    resize_keyboard=True
)

settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🗒 My information"),
        ],
        [
            KeyboardButton(text = "◀️ Back")
        ]
    ],
    resize_keyboard=True
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "📞 Send phone number", request_contact=True)
        ]
    ],
    resize_keyboard=True
)