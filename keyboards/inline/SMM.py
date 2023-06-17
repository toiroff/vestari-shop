from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


qator_raqamlari = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "1️⃣",
                callback_data = "bittalik"
            ),
            InlineKeyboardButton(
                text = "2️⃣",
                callback_data = "ikkitalik"
            ),
            InlineKeyboardButton(
                text = "3️⃣",
                callback_data = "uchtalik"
            ),
        ],
        [
            InlineKeyboardButton(
                text = "4️⃣",
                callback_data = "torttalik"
            ),
            InlineKeyboardButton(
                text = "5️⃣",
                callback_data = "beshtalik"),
        ],
        [
            InlineKeyboardButton(
                text = "↪️ Orqaga",
                callback_data="back_to_panel"
            ),
        ],
    ]
)