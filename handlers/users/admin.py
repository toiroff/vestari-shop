from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, ContentType

from data.config import ADMINS
from keyboards.default.menu import contact, main
from keyboards.inline.SMM import qator_raqamlari
from keyboards.inline.admin_panel import panel, edit_bot, base_download, kb, delete_tarmoq_admin, orders_btns, \
    delete_products_admin, edit_products_admin, EDIT_maxsulot, delete_category_admin, select_category_admin
from keyboards.inline.product import products_keyboard, buy_keyboard, numberorder, check_of_order, yes_no, acceptance, \
    buttons_for_basket, category_keyboard
from loader import dp, bot, db
from states.state import *


@dp.message_handler(commands = ['X'], chat_id = ADMINS)
async def enter_panel(message: types.Message):
	await message.answer("You are in the admin panel", reply_markup = panel)
	await message.delete()

# Botni tahrirlash tugmasi uchun handler
@dp.callback_query_handler(text = "edit_bot")
async def edit_bot_adm(call: CallbackQuery):
	await call.message.edit_reply_markup(reply_markup = edit_bot)

@dp.callback_query_handler(text = "close_panel")
async def close_admin(call: CallbackQuery):
	await call.message.answer("<i>Main menu</i>", reply_markup = main)
	await call.message.delete()

@dp.callback_query_handler(text = "back_to_panel")
async def bacjk_topanel(call: CallbackQuery):
	await call.message.answer(text = "You are in the admin panel!",reply_markup = panel)
	await call.message.delete()

@dp.callback_query_handler(text="download_base")
async def dwn_base(call: CallbackQuery):
	await call.message.edit_reply_markup(reply_markup=base_download)


@dp.callback_query_handler(text = "statistics")
async def statistika(call: CallbackQuery):
	products = db.count_products()[0][0]
	users = db.count_users()[0]
	await call.answer(text = f"📊 Users: {users}!\n\n🛍 Products: {products} !", show_alert = True)

@dp.callback_query_handler(text = "edit_mes")
async def endit_media(call: CallbackQuery):
	await call.message.edit_reply_markup(reply_markup=kb.messages())

@dp.callback_query_handler(text="Tarmoq_add",chat_id=ADMINS)
async def orders(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>🔵 Enter network name</b>\n\n<i>Example : 🔵 Telegram</i>")
    await Add_tarmoq.name.set()

@dp.message_handler(state=Add_tarmoq.name)
async def add_tarmoq_name(message:types.Message, state:FSMContext):
    await state.update_data({"name":message.text})
    await message.answer("<b>Enter network url</b>\n<i>Example :</i> <code>https://t.me/Coodehub</code>")
    await Add_tarmoq.url.set()

@dp.message_handler(state=Add_tarmoq.url)
async def add_tarmoq_name(message: types.Message, state: FSMContext):
    await state.update_data({"url": message.text})
    malumot = await state.get_data()
    name = malumot.get("name")
    url = malumot.get("url")
    try:
        db.add_tarmoq(name=name,url=url)
    except:
        pass
    await message.answer(text="Added to Network List ! ✔️")
    await bot.send_message(chat_id=message.from_user.id,text="Admin menu",reply_markup=panel)
    await state.finish()

@dp.callback_query_handler(text="Tarmoq_del",chat_id=ADMINS)
async def del_products(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("🗑 Just click on the Network you want to delete",reply_markup=await delete_tarmoq_admin())


@dp.callback_query_handler(text_contains="admin_del_tarmoq:")
async def delet_orders(call:types.CallbackQuery):
    data = call.data.rsplit(":")
    delete_orders = db.delete_tarmoq_admin(data[1])
    await call.answer("🗑 Deleted network !",show_alert=True)
    await call.message.delete()
    await call.message.answer("Turn it off again ?",reply_markup=await delete_tarmoq_admin())

@dp.callback_query_handler(text="aloqa",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    admin_malumot = db.select_all_admin()
    for x in admin_malumot:

        text = f"Your information\n\n"
        text += f"<i>👤 Contact Online Admin :</i> <b>{x[2]}\n</b>"
        text += f"<i>📞 phone number :</i> <b>+{x[1]}</b>"
        await call.message.delete()
        await call.message.answer(text=text,reply_markup=kb.admin_aloqa())

@dp.callback_query_handler(text="Admin_edit")
async def edit(call: types.CallbackQuery):
    await call.message.answer("Enter Admin User Eg: <code>@UmarDeveloper</code>")
    await Update_admin.name.set()

@dp.message_handler(state=Update_admin.name)
async def bot_echo(message:types.Message,state:FSMContext):
    full_name = message.text
    await state.update_data({"full_name": full_name})
    malumot = await state.get_data()
    db.update_full_name_admin(user_id=message.from_user.id,url=malumot.get("full_name"))
    await message.reply("✅ Admin user Updated.")
    await state.finish()
    admin_malumot = db.select_all_admin()
    for x in admin_malumot:

        text = f"Your information\n\n"
        text += f"<i>👤 Contact Online Admin :</i> <b>{x[2]}\n</b>"
        text += f"<i>📞 phone number :</i> <b>+{x[1]}</b>"
        await message.answer(text,reply_markup=kb.admin_aloqa())


@dp.callback_query_handler(text="admin_number_edit")
async def edit(call: types.CallbackQuery):
    await call.message.answer("Enter your phone number :",reply_markup=kb.contact())
    await Update_admin.number.set()

@dp.message_handler(content_types=['contact'], state=Update_admin.number)
async def add_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data({"phone_number": phone_number})
    malumot = await state.get_data()
    db.update_full_number_admin(user_id=message.from_user.id, number=malumot.get("phone_number"))
    await message.reply("✅ Your phone number has been updated.",reply_markup = ReplyKeyboardRemove())
    await state.finish()
    admin_malumot = db.select_all_admin()
    for x in admin_malumot:
        text = f"Your information\n\n"
        text += f"<i>👤 Contact Online admin :</i> <b>{x[2]}\n</b>"
        text += f"<i>📞 Phone number :</i> <b>+{x[1]}</b>"
        await message.answer(text,reply_markup=kb.admin_aloqa())


@dp.callback_query_handler(text="type_db")
async def orders(call: types.CallbackQuery):
    file = types.InputFile(path_or_bytesio = "main.db")
    await call.message.delete()
    await bot.send_document(chat_id = ADMINS[0], document = file, caption = "Database 🗄")
    await call.message.answer(f"<b>👨🏻‍💻 In the admin panel</b>",reply_markup=panel)


# Mahsulotlar qatorini tahrirlash uchun
@dp.callback_query_handler(text = "edit_qator")
async def edit_qator_raqamlari(call: CallbackQuery):
    await call.message.answer(text = "How many rows should the products be placed in?", reply_markup = qator_raqamlari)
    await call.message.delete()


@dp.callback_query_handler(text = "bittalik")
async def edit_raqam(call: CallbackQuery):
    try:
        db.update_qator(number = 1)
        await call.message.answer("Successfully updated!")
        await call.message.edit_reply_markup(reply_markup = panel)
    except Exception as err:
        pass
        await call.message.edit_reply_markup(reply_markup = panel)

@dp.callback_query_handler(text = "ikkitalik")
async def edit_rfggaqam(call: CallbackQuery):
    try:
        db.update_qator(number = 2)
        await call.message.answer("Successfully updated!")
        await call.message.edit_reply_markup(reply_markup = panel)
    except Exception as err:
        pass
        await call.message.edit_reply_markup(reply_markup = panel)

@dp.callback_query_handler(text = "uchtalik")
async def edit_rdfdfaqam(call: CallbackQuery):
    try:
        db.update_qator(number = 3)
        await call.message.answer("Successfully updated!")
        await call.message.edit_reply_markup(reply_markup = panel)
    except Exception as err:
        pass
        await call.message.edit_reply_markup(reply_markup = panel)

@dp.callback_query_handler(text = "torttalik")
async def edit_SDraqam(call: CallbackQuery):
    try:
        db.update_qator(number = 4)
        await call.message.answer("Successfully updated!")
        await call.message.edit_reply_markup(reply_markup = panel)
    except Exception as err:
        pass
        await call.message.edit_reply_markup(reply_markup = panel)

@dp.callback_query_handler(text = "beshtalik")
async def edit_rSDFaqam(call: CallbackQuery):
    try:
        db.update_qator(text = 5)
        await call.message.answer("Successfully updated!")
        await call.message.edit_reply_markup(reply_markup = panel)
    except Exception as err:
        pass
        await call.message.edit_reply_markup(reply_markup = panel)


@dp.callback_query_handler(text = "orders")
async def orders_bt(call: CallbackQuery):
    try:
        await call.message.edit_reply_markup(reply_markup=orders_btns)
    except Exception as err:
        await bot.send_message(chat_id=ADMINS[0], text = err)



@dp.callback_query_handler(text = "accepted")
async def get_acceptes_orders(call: CallbackQuery):
    if db.status_orders(status="accept"):
        datas = db.status_orders(status="accept")
        for data in datas:
            print(data[4])
            text = ""
            id_order = data[0]
            text += f"🔢 Order number: {data[0]}\n"
            text += f"📆 The date: {data[4]}\n"
            text += f"📱 Customer's phone number: +{data[3]}\n"
            text += "🟢 Order status: Accepted ✅\n\n"
            m = db.datas_detail(order_id = id_order)
            print(m)
            son = 0
            total_price = 0
            for n in m:
                product_id = n[2]
                number = n[3]
                products = db.get_product(id = product_id)
                product_name = products[1]
                product_price = products[3]
                son += 1
                text += f"{son}.Product name: {product_name}\n"
                price = int(number) * int(product_price)
                text += f"{number} x {product_price} = {price} $\n\n"
                total_price += price
            text += f"💸 Total {total_price} $"
            await call.message.answer(text = text)
        await call.message.answer(text = "Admin panel", reply_markup=panel)
        await call.message.delete()
    else:
        await call.answer("✅ No confirmed orders available.")


@dp.callback_query_handler(text = "rejected")
async def get_acceptes_orders(call: CallbackQuery):
    if db.status_orders(status="reject"):
        datas = db.status_orders(status="reject")
        for data in datas:
            print(data[4])
            text = ""
            id_order = data[0]
            text += f"🔢 Order number: {data[0]}\n"
            text += f"📆 Date: {data[4]}\n"
            text += f"📱 Customer's phone number: +{data[3]}\n"
            text += "🔴 Order status: rejected ❌\n\n"
            m = db.datas_detail(order_id = id_order)
            print(m)
            son = 0
            total_price = 0
            for n in m:
                product_id = n[2]
                number = n[3]
                products = db.get_product(id = product_id)
                product_name = products[1]
                product_price = products[3]
                son += 1
                text += f"{son}.Product name: {product_name}\n"
                price = int(number) * int(product_price)
                text += f"{number} x {product_price} = {price} $\n\n"
                total_price += price
            text += f"💸 Total: {total_price} $"
            await call.message.answer(text = text)
        await call.message.answer(text = "Admin panel", reply_markup=panel)
        await call.message.delete()
    else:
        await call.answer("❌ There are no rejected orders.")


@dp.callback_query_handler(text = "waiting")
async def get_acceptes_orders(call: CallbackQuery):
    if db.status_orders(status="waiting"):
        datas = db.status_orders(status="waiting")
        for data in datas:
            print(data[4])
            text = ""
            id_order = data[0]
            text += f"🔢 Order number: {data[0]}\n"
            text += f"📆 Date: {data[4]}\n"
            text += f"📱 Customer's phone number: +{data[3]}\n"
            text += "🟣 Order status : Waiting ⏳\n\n"
            m = db.datas_detail(order_id = id_order)
            print(m)
            son = 0
            total_price = 0
            for n in m:
                product_id = n[2]
                number = n[3]
                products = db.get_product(id = product_id)
                product_name = products[1]
                product_price = products[3]
                son += 1
                text += f"{son}.Product name: {product_name}\n"
                price = int(number) * int(product_price)
                text += f"{number} x {product_price} = {price} $\n\n"
                total_price += price
            text += f"💸 Total: {total_price} $"
            await call.message.answer(text = text)
        await call.message.answer(text = "Admin panel", reply_markup=panel)
        await call.message.delete()
    else:
        await call.answer("⏳ There are no pending orders.")


@dp.callback_query_handler(text="edit_products",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>🛍 Product settings</b>",reply_markup=kb.shop())


#  Mahsulot qo'shish func
@dp.callback_query_handler(text="Mahsulot_add",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>which category you want to add to</b>",reply_markup= await select_category_admin())
    await Add_products.category.set()
@dp.callback_query_handler(state=Add_products.category)
async def bot_menu(message:types.CallbackQuery,state:FSMContext):
    ctg = message.data
    category = ctg.replace('category:', '')
    await state.update_data({'category':category})

    await message.message.answer("<b>🛍 Enter product name</b>\n\n<i>Example : Nike</i>")
    await Add_products.name.set()
    await message.message.delete()


@dp.message_handler(state=Add_products.name)
async def add_name(message:types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("<b>💸 Enter price\n\n please type in $ just don't put the $ sign</b>")
    await Add_products.money.set()

@dp.message_handler(state=Add_products.money)
async def add_name(message:types.Message, state: FSMContext):
    await state.update_data({"money": message.text})
    await message.answer("<b>ℹ️ Enter product information</b>")
    await Add_products.info.set()

@dp.message_handler(state=Add_products.info)
async def add_name(message:types.Message, state: FSMContext):
    await state.update_data({"info": message.text})
    await message.answer("<b>🖼 Send a photo...</b>")
    await Add_products.photo.set()

@dp.message_handler(state=Add_products.photo, content_types=ContentType.PHOTO)
async def add_name(message:types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    print(file_id)
    await state.update_data({"photo": file_id})
    malumot = await state.get_data()
    name = malumot.get("name")
    money = malumot.get("money")
    info = malumot.get("info")
    photo = malumot.get("photo")
    category = malumot.get('category')


    text = f"📄 Name: {name}\n"
    text += f"📜 Category: {category}\n"
    text += f"💰 Price: {money} $\n"
    text += f"📋 Information:👇👇👇\n\n"
    text += f"{info}\n\n"
    text += f"<i>Do you approve the product? ?</i>"
    await bot.send_photo(chat_id=message.from_user.id,photo=photo,caption=text,reply_markup=kb.check())
    await Add_products.check.set()



@dp.callback_query_handler(text="check_mah",state=Add_products.check)
async def add_name(call:types.CallbackQuery, state: FSMContext):
    malumot = await state.get_data()
    name = malumot.get("name")
    money = malumot.get("money")
    info = malumot.get("info")
    photo = malumot.get("photo")
    category = malumot.get('category')

    user_id = call.from_user.id

    db.add_products(product_name=name,product_money=money,product_photo=photo,product_about=info,product_category=category)
    # except:
    #     pass
    await call.answer(text="Released to Sel ! ✔️", show_alert=True)
    await bot.send_message(chat_id=user_id,text="Admin menu",reply_markup=panel)
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(text="off_mah",state=Add_products.check)
async def add_name(call:types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.answer(text="❌ Canceled.", show_alert=True)
    await bot.send_message(chat_id=user_id,text="Admin menu",reply_markup=panel)
    await call.message.delete()
    await state.finish()
# ADD CATEGORY ----------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="category_add")
async def bot_menu(message:types.CallbackQuery):
    await message.message.answer('Enter a category name')
    await message.message.delete()
    await Add_category.name.set()

@dp.message_handler(state=Add_category.name)
async def bot_menu(message:types.Message,state:FSMContext):
    await message.delete()
    await state.update_data({'name':message.text})
    await message.answer(f'Category: <b>{message.text}</b>\n\n'
                         f'Do you agree ?',reply_markup=yes_no)
    await Add_category.check.set()
@dp.callback_query_handler(state=Add_category.check, text="XA")
async def bot_menu(message:types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    name = data.get('name')
    try:
        db.add_category(name=name)
    except:
        pass
    await message.answer('Successfully added',show_alert=True)
    await bot.send_message(chat_id=message.from_user.id,text="Admin menu",reply_markup=panel)
    await message.message.delete()
    await state.finish()

@dp.callback_query_handler(state=Add_category.check,text="YOQ")
async def bot_menu(call:types.CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await call.answer(text="❌ Canceled.", show_alert=True)
    await bot.send_message(chat_id=user_id, text="Admin menu", reply_markup=panel)
    await call.message.delete()
    await state.finish()
# DELETE CATEGORY --------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="category_del",chat_id=ADMINS)
async def bot_menu(message:types.CallbackQuery):
    await message.message.delete()
    await message.message.answer("🗑 Just click on the category you want to remove",
                              reply_markup=await delete_category_admin())

@dp.callback_query_handler(text_contains="admin_del_category:")
async def delet_orders(call:types.CallbackQuery):
    data = call.data.rsplit(":")

    delete = db.delete_category(id=data[1])

    await call.answer("🗑Category deleted !",show_alert=True)
    await call.message.delete()
    await call.message.answer("Turn it off again ?",reply_markup=await delete_category_admin())

# Mahsulot o'chirish func -------------------------------------------------------------------------------------
@dp.callback_query_handler(text="Mahsulot_del",chat_id=ADMINS)
async def del_products(call: types.CallbackQuery):
    await call.message.answer("🗑 Just click on the product you want to remove",reply_markup=await delete_products_admin())

@dp.callback_query_handler(text_contains="admin_del_products:")
async def delet_orders(call:types.CallbackQuery):
    data = call.data.rsplit(":")
    print(data)
    delete_orders = db.delete_order_admin(data[1])
    delete = db.delete_order(order_id=data[1])
    delete_details = db.delete_order_details(order_id=data[1])
    await call.answer("🗑Product deleted !",show_alert=True)
    await call.message.delete()
    await call.message.answer("Turn it off again ?",reply_markup=await delete_products_admin())


# Mahsulot edit func
@dp.callback_query_handler(text="Mahsulot_edit",chat_id=ADMINS)
async def del_products(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("📝 Just click on the product you want to edit",reply_markup=await edit_products_admin())




@dp.callback_query_handler(text_contains = "admin_edit_products:")
async def procs(call: types.CallbackQuery):
    data = call.data
    id = data.replace('admin_edit_products:','')
    prods = db.get_product(
        id=id
    )
    await call.message.delete()
    text = f"📄 Name: {prods[1]}\n"
    text += f"Category: {prods[5]}\n"
    text += f"💰 Price: {prods[3]}\n"
    text += f"📋 Information:👇👇👇\n\n{prods[4]}"
    photo = f"{prods[2]}"
    keyb = await EDIT_maxsulot(id)
    await call.message.answer_photo(photo = photo,caption=text, reply_markup=keyb)

@dp.callback_query_handler(text_contains="ctg_edt:")
async def procs(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    id = data.replace('ctg_edt:', '')
    await state.update_data({"name": id})
    await call.message.answer("Select product category",reply_markup= await select_category_admin())
    await Update_category.name.set()
    await call.message.delete()

@dp.callback_query_handler(state=Update_category.name)
async def bot_echo(message: types.CallbackQuery, state: FSMContext):

    full_name = message.data
    await state.update_data({"full_name": full_name})
    malumot = await state.get_data()
    db.update_category_max(id=malumot.get("name"),  category=malumot.get("full_name"))
    await message.message.reply("✅ Product category updated.")
    await state.finish()
    await message.message.answer("Admin Panel", reply_markup=panel)
    await message.message.delete()




@dp.callback_query_handler(text_contains = "name_edt:")
async def procs(call: types.CallbackQuery,state:FSMContext):
    data = call.data
    id = data.replace('name_edt:','')
    await state.update_data({"name": id})
    await call.message.answer("Enter product name")
    await Update_max_name.name.set()

@dp.message_handler(state=Update_max_name.name)
async def bot_echo(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data({"full_name": full_name})
    malumot = await state.get_data()
    db.update_full_name_max(id=malumot.get("name"), product_name=malumot.get("full_name"))
    await message.reply("✅ Product Name Updated.")
    await state.finish()
    await message.answer("Admin Panel", reply_markup=panel)



@dp.callback_query_handler(text_contains = "money_edt:")
async def procs(call: types.CallbackQuery,state:FSMContext):
    data = call.data
    id = data.replace('money_edt:','')
    await state.update_data({"name": id})
    await call.message.answer("Enter a price")
    await Update_max_money.name.set()

@dp.message_handler(state=Update_max_money.name)
async def bot_echo(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data({"full_name": full_name})
    malumot = await state.get_data()
    db.update_money_max(id=malumot.get("name"), product_money=malumot.get("full_name"))
    await message.reply("✅ Product Price Updated.")
    await state.finish()
    await message.answer("Admin Panel", reply_markup=panel)



@dp.callback_query_handler(text_contains = "about_edt:")
async def procs(call: types.CallbackQuery,state:FSMContext):
    data = call.data
    id = data.replace('about_edt:','')
    await state.update_data({"name": id})
    await call.message.answer("Enter product information")
    await Update_max_about.name.set()

@dp.message_handler(state=Update_max_about.name)
async def bot_echo(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data({"full_name": full_name})
    malumot = await state.get_data()
    db.update_money_about(id=malumot.get("name"), product_about=malumot.get("full_name"))
    await message.reply("✅ Product Updated.")
    await state.finish()
    await message.answer("Admin Panel", reply_markup=panel)


@dp.callback_query_handler(text_contains = "photo_edt:")
async def procs(call: types.CallbackQuery,state:FSMContext):
    data = call.data
    id = data.replace('photo_edt:','')
    await state.update_data({"name": id})
    await call.message.answer("Enter product photo.")
    await Update_max_photo.name.set()


@dp.message_handler(state=Update_max_photo.name, content_types=ContentType.PHOTO)
async def add_name(message:types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data({"photo": file_id})
    malumot = await state.get_data()
    photo = malumot.get("photo")
    db.update_photo_max(id=malumot.get("name"), product_photo=photo)
    await message.reply("✅ Product updated.")
    await state.finish()
    await message.answer("Admin Panel", reply_markup=panel)







@dp.callback_query_handler(text="send_post",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    use = await bot.get_me()
    await call.message.answer(f"<b>Message Types 1-3 \n\n</b>"
                              f"1. FORWARD MESSAGE (@{call.from_user.username})\n"
                              f"2. COPY MESSAGE (@{call.from_user.username})\n"
                              f"3. POST MESSAGE CREATED BY A BOT (@{use.username})",reply_markup=kb.admin_send_all())


# Forward Xabar Yuborish
@dp.callback_query_handler(text="bir_send",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    use = await bot.get_me()
    await call.message.answer("<b>Messaga types 1-6 \n\n</b>"
                              "1. Text Message \n"
                              "2. Audio Message \n"
                              "3. Video Message\n"
                              "4. Document Message\n"
                              "5. Voice Message\n"
                              "6. Photo Message",reply_markup=kb.admin_send_forward())

@dp.callback_query_handler(text= "bir_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("ENTER YOUR MESSAGE. (FORWARD MESSAGE TYPE TEXT)")
    await send_text.name.set()

@dp.message_handler(state=send_text.name)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text= "olt_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter a message (FORWARD MESSAGE TYPE PHOTO)")
    await send_photo.name.set()

@dp.message_handler(state=send_photo.name,content_types=ContentType.PHOTO)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


@dp.callback_query_handler(text= "uch_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter a message. (FORWARD MESSAGE TYPE VIDEO)")
    await send_video.name.set()

@dp.message_handler(state=send_video.name,content_types=ContentType.VIDEO)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


@dp.callback_query_handler(text= "tort_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter a message. (FORWARD MESSAGE TYPE DOCUMENT)")
    await send_doc.name.set()

@dp.message_handler(state=send_doc.name,content_types=ContentType.DOCUMENT)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text= "besh_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("enter message. (FORWARD MESSAGE TYPE VOICE)")
    await send_voice.name.set()

@dp.message_handler(state=send_voice.name,content_types=ContentType.VOICE)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


@dp.callback_query_handler(text= "ikki_sendf")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (FORWARD MESSAGE TYPE AUDIO)")
    await send_audio.name.set()

@dp.message_handler(state=send_audio.name,content_types=ContentType.AUDIO)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.forward_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


# COPY XABAR UCHUN
@dp.callback_query_handler(text="ikki_send",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    use = await bot.get_me()
    await call.message.answer("<b>Xabar Turlari 1-6  (COPY MESSAGE TYPE)\n\n</b>"
                              "1. Text \n"
                              "2. Audio \n"
                              "3. Video \n"
                              "4. Document \n"
                              "5. Voice \n"
                              "6. Photo ",reply_markup=kb.admin_send_copy())


@dp.callback_query_handler(text= "bir_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE TEXT)")
    await send_ctext.name.set()

@dp.message_handler(state=send_ctext.name,content_types=ContentType.TEXT)
async def forworad(message:types.Message, state:FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


@dp.callback_query_handler(text="ikki_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE AUDIO)")
    await send_caudio.name.set()


@dp.message_handler(state=send_caudio.name,content_types=ContentType.AUDIO)
async def forworad(message: types.Message, state: FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text="uch_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE VIDEO)")
    await send_cvideo.name.set()


@dp.message_handler(state=send_cvideo.name,content_types=ContentType.VIDEO)
async def forworad(message: types.Message, state: FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text="tort_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE DOCUMENT)")
    await send_cdoc.name.set()


@dp.message_handler(state=send_cdoc.name,content_types=ContentType.DOCUMENT)
async def forworad(message: types.Message, state: FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()


@dp.callback_query_handler(text="besh_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE VOICE)")
    await send_cvoice.name.set()


@dp.message_handler(state=send_cvoice.name,content_types=ContentType.VOICE)
async def forworad(message: types.Message, state: FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text="olt_sendc")
async def Forward(call: types.CallbackQuery):
    await call.message.answer("Enter message. (COPY MESSAGE TYPE PHOTO)")
    await send_cphoto.name.set()


@dp.message_handler(state=send_cphoto.name,content_types=ContentType.PHOTO)
async def forworad(message: types.Message, state: FSMContext):
    user_id = db.select_all_message()
    for x in user_id:
        userid = x[1]
        try:
            await bot.copy_message(
                chat_id=userid,
                from_chat_id=message.chat.id,
                message_id=message.message_id)
        except:
            pass
        await state.finish()

@dp.callback_query_handler(text="uch_send",chat_id=ADMINS)
async def orders(call: types.CallbackQuery):
    await call.message.delete()
    use = await bot.get_me()
    await call.message.answer("<b>Message types 1-6 (Message type bot)\n\n</b>"
                              "1. Text \n"
                              "2. Audio \n"
                              "3. Video \n"
                              "4. Document \n"
                              "5. Voice \n"
                              "6. Photo ",reply_markup=kb.admin_send_bot())