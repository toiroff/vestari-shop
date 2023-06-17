from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart,CommandHelp

from data.config import ADMINS
from keyboards.default.menu import *
from keyboards.inline.menu import *
from loader import dp, bot, db
from states.state import *



# /start komandasi uchun handler
@dp.message_handler(CommandStart(), state = "*")
async def bot_start(message: types.Message):
    try:
        try:
            db.add_message(user_id=ADMINS[0])
        except:
            pass
        if db.check_user(user_id=message.from_user.id):
            await message.answer(f"Hi, {message.from_user.get_mention()}", reply_markup=main)
        else:
            await message.answer(f"Hi, {message.from_user.full_name}!\nPlease, Enter your name:")
            await RegisterState.name.set()
    except Exception as err:
        await bot.send_message(chat_id=ADMINS[0],text = err)

@dp.message_handler(state = RegisterState.name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name":name})
    await message.answer("Click the Send phone number button :)", reply_markup=contact)
    await RegisterState.next()

@dp.message_handler(content_types='contact', state = RegisterState.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    phone_num = message.contact.phone_number
    data = await state.get_data()
    try:
        db.add_user(user_id=message.from_user.id,
            username=message.from_user.username,
            fullname=data['name'],
            phone=phone_num)
        await message.answer("You have successfully registered!", reply_markup=main)
        await state.finish()
        for admin in ADMINS:
            await bot.send_message(chat_id = admin, text = f"🎉 New user.\nAdded {message.from_user.get_mention()} base.\nID: {message.from_user.id}\nUsername: @{message.from_user.username}\nThere are  {db.count_users()[0]} users in base.")
    except Exception as err:
        print(err)
        await state.finish()


# Button
@dp.message_handler(text = "⚙️ Settings")
async def settings1(message: types.Message):
    await message.answer("<b>⚙️ Settings</b>", reply_markup=settings)
    await message.delete()

# Sozlamalarda orqaga qaytish
@dp.message_handler(text = "◀️ Back")
async def back_main(message: types.Message):
    await message.answer("<i>Main menu</i>", reply_markup=main)
    await message.delete()


# Sozlamalar (inline) orqaga qaytish
@dp.callback_query_handler(text_contains = "back_settings")
async def back_setting(call: types.CallbackQuery):
    await call.message.answer("<i>Main menu!</i>", reply_markup=main)
    await call.message.delete()


# Sozlamalar
@dp.message_handler(text = "🗒 My information")
async def get_datas(message: types.Message):
    user = db.get_data_user(user_id=message.from_user.id)
    await message.delete()
    await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                        reply_markup=DATAS
    )

@dp.callback_query_handler(text_contains = "editdata")
async def edit_data(call: types.CallbackQuery):
    await call.message.delete()
    user = db.get_data_user(
        user_id=call.from_user.id
    )
    await call.message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                            reply_markup=EDITDATAS
    )

# Foydalanuvchi ismini tahrirlash uchun handler
@dp.callback_query_handler(text_contains = "edit_name", state = None)
async def change_name(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Enter your full name")
    await edit_name.name.set()

# State
@dp.message_handler(state = edit_name.name)
async def change_nm(message: types.Message, state: FSMContext):
    text = message.text
    if text == "🗒 My information":
        user = db.get_data_user(user_id=message.from_user.id)
        await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                            reply_markup=DATAS)
        await state.finish()
    elif text == "◀️ Back":
        await message.answer("<i>Main menu!</i>", reply_markup=main)
        await state.finish()
    else:
        try:
            db.update_name(fullname=text,
                user_id=message.from_user.id)
            await message.reply(text="✅ Your name have been updated.")
            user = db.get_data_user(user_id=message.from_user.id)
            await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                                 reply_markup=DATAS)
            await state.finish()
        except Exception as err:
            print(err)
            await state.finish()

# Foydalanuvchi telefon raqamini tahrirlash uchun handler
@dp.callback_query_handler(text_contains = "edit_phone", state = None)
async def change_phone(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Enter your phone number: ", reply_markup=contact)
    await edit_number.phone.set()

# State
@dp.message_handler(state = edit_number.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    text = message.text
    if text == "🗒 My information":
        user = db.get_data_user(user_id=message.from_user.id)
        await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                            reply_markup=DATAS)
        await state.finish()
    elif text == "◀️ Back":
        await message.answer("<i>Main menu!</i>", reply_markup=main)
        await state.finish()
    else:
        try:
            db.update_phone(phone=text,
                            user_id=message.from_user.id)
            await message.reply(text="✅ Your phone number has been updated.")
            user = db.get_data_user(user_id=message.from_user.id)
            await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                            reply_markup=DATAS)
            await state.finish()
        except Exception as err:
            print(err)
            await state.finish()

# Contact
@dp.message_handler(state = edit_number.phone, content_types='contact')
async def change_p(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    db.update_phone(phone=phone,
        user_id=message.from_user.id)
    await message.reply(text="✅ Your phone number has been updated.", reply_markup = settings)
    user = db.get_data_user(user_id=message.from_user.id)
    await message.answer("Your information\n\n"
                        f"👤 <i>Your name:</i> <b>{user[0]}</b>\n"
                        f"📞 <i>Your phone number:</i> <b>+{user[1]}</b>",
                    reply_markup=DATAS)
    await state.finish()

#Ijtimoyi tarmoqlatrimiz
@dp.message_handler(text="🔵 Biz ijtimoiy tarmoqlarda")
async def show_menu(message: types.Message):
    markup = await messages()
    await message.answer(text="Bizning Rasmiy Saxifalarimiz.", reply_markup=markup)
    await message.delete()


#Biz bilan boglanish
@dp.message_handler(text="📞 Contact us")
async def show_menu(message: types.Message):
    admin_malumot = db.select_all_admin()

    for x in admin_malumot:
        text = f"👩🏻‍💻Contact us :\n\n"
        text += f"<i>👨🏻‍💻Online admin:</i> <b>{x[2]}\n</b>"
        text += f"<i>📲 phone number :</i> <b>+{x[1]}</b>"
        await message.answer(text=text)
        await message.delete()

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - Start the bot",
            "/help - Help")

    await message.answer("\n".join(text))

# Echo
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)