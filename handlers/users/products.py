from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.menu import contact, main
from keyboards.inline.product import products_keyboard, buy_keyboard, numberorder, check_of_order, yes_no, acceptance, \
    buttons_for_basket,category_keyboard
from loader import dp, bot, db
from states.state import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Savat tugmasi bosilganda ishlaydigan handler
@dp.message_handler(text = "🛒 Basket")
async def show_basket(message: types.Message):
    try:
        total_price = 0
        text = "🛒 Savat\n\n"
        son = 0
        if db.datas_from_basket(user_id=message.from_user.id):
            datas = db.datas_from_basket(user_id=message.from_user.id)
            for data in datas:
                son += 1
                book_id = (data[1])
                number = (data[2])
                products = db.get_product(id=book_id)
                narx = int(number) * int(products[3])
                total_price += narx
                text += f"{son}. {products[1]}\n"
                text += f"{number} x {products[3]} = {float(narx)} so'm\n\n"
            text += f"Jami: {float(total_price)} so'm."
            await message.answer(text = text, reply_markup = await buttons_for_basket())
        else:
            await message.answer("🛒 Your cart is empty!")
    except Exception as err:
        await message.answer(f"Error: {err}")


# Mahsulotlar chiqrish uchun
@dp.message_handler(text="🛍 Products")
async def show_menu(message: types.Message):

    markup = await category_keyboard()
    await message.answer('Select category',reply_markup=markup)
    await message.delete()
    # await Category.category.set()


@dp.callback_query_handler(text_contains = "category:")
async def bot_menu(message: types.CallbackQuery):
    global category
    data = message.data
    category = data.replace('category:', '')
    g = db.select_menu()
    global markup
    for i in g:
        raqam = int(f"{i[1]}")
        markup = InlineKeyboardMarkup(row_width=raqam)
    products = db.get_products(category=category)
    for product in products:
        button_text = f"{product[1]}"
        callback_data = f"mahsulot:{product[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(
            InlineKeyboardButton(text="◀️ Back",callback_data='category_back')
        )



    await message.message.edit_text("Select a product", reply_markup=markup)



@dp.callback_query_handler(text="product_back")
async def bot_menu(message:types.CallbackQuery,state:FSMContext):
    await message.message.answer("<i>Main menu</i>", reply_markup=main)
    await state.finish()
    await message.message.delete()

@dp.callback_query_handler(text="category_back")
async def bot_menu(message:types.CallbackQuery):
 

    markup = await category_keyboard()
    await message.message.edit_text('Select category', reply_markup=markup)





#Bitta mahsulotni tanlaganda ishlaydigan handler
@dp.callback_query_handler(text_contains = "mahsulot:")
async def procs(call: types.CallbackQuery):
    data = call.data
    id = data.replace('mahsulot:','')
    prods = db.get_product(
        id=id
    )
    await call.message.delete()
    text = f"📄 Name: {prods[1]}\n"
    text += f"💰 Price: {prods[3]} CHF\n"
    text += f"📋 About:👇👇👇\n\n{prods[4]}"
    photo = f"{prods[2]}"
    keyb = await buy_keyboard(product_id = f"{id}")
    await call.message.answer_photo(photo = photo,caption=text, reply_markup=keyb)

# Mahsulotlarni qaytarganda orqaga qaytish uchun
@dp.callback_query_handler(text_contains = "orqaga")
async def show_menu(call: types.CallbackQuery):
    g = db.select_menu()
    global markup
    for i in g:
        raqam = int(f"{i[1]}")
        markup = InlineKeyboardMarkup(row_width=raqam)
    products = db.get_products(category=category)
    for product in products:
        button_text = f"{product[1]}"
        callback_data = f"mahsulot:{product[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(
        InlineKeyboardButton(text="◀️ Back", callback_data='category_back')
    )
    await call.message.delete()
    await call.message.answer("Select a product", reply_markup=markup)
    # await call.message.delete()
    # markupc =  products_keyboard()
    # await call.message.answer("Select a product", reply_markup=markup)

#Mahsulot tanlash uchun
@dp.callback_query_handler(text_contains = "get:")
async def get_produzsdct(call: types.CallbackQuery):
    id_product = call.data.replace("get:","")
    mahsulot = db.get_product(id = id_product)
    name = f"{mahsulot[1]}"
    rasm = mahsulot[2]
    narx = f"{mahsulot[3]}"
    text = f"🛍 <b>Name:</b> <i>{name}</i>\n"
    text += f"💸 <b>Price:</b> <i>{narx}</i>CHF\n\n"
    text += f"<b>How many of this product would you like to order??</b>"
    markup = await numberorder(id=id_product, volume=1)
    await call.message.answer_photo(photo = rasm, caption=text, reply_markup=markup)
    await call.message.delete()


# Mahsulot qoshish uchun
@dp.callback_query_handler(text_contains = "plus")
async def plus_number(call: types.CallbackQuery):
    data = call.data.rsplit(':')
    num = int(data[2])
    num += 1
    markup = await numberorder(id = data[1], volume=num)
    await call.message.edit_reply_markup(reply_markup=markup)

# MAhsulot ayirish uchun
@dp.callback_query_handler(text_contains = "minus")
async def minus_number(call: types.CallbackQuery):
    data = call.data.rsplit(':')
    num = int(data[2])
    if num == 1:
        await call.answer("You can buy at least one product! 😉", show_alert=True)
    elif num>1:
        num -= 1
        markup = await numberorder(id = data[1], volume=num)
        await call.message.edit_reply_markup(reply_markup=markup)

# #Tanlagan Mhsulotiga qaytish uchun
@dp.callback_query_handler(text_contains = "Orqaga:")
async def back_book(call: types.CallbackQuery):
    data = call.data
    id = data.replace('Orqaga:','')
    prods = db.get_product(id=id)
    text = f"📄 Name: {prods[1]}\n"
    text += f"💰 Price: {prods[3]}CHF\n"
    text += f"📋 About:👇👇👇\n\n{prods[4]}"
    photo = f"{prods[2]}"
    keyb = await buy_keyboard(product_id = f"{id}")
    await call.message.answer_photo(photo = photo,caption=text, reply_markup=keyb)
    await call.message.delete()

# Savatga qo'shish tugmasi uchun handler
@dp.callback_query_handler(text_contains = "savat")
async def add_product(call: types.CallbackQuery):
    data = call.data.rsplit(':')
    try:
        if db.check_order_id(order_id=f"{data[1]}", user_id=call.from_user.id):
            db.update_number(number=f"{data[2]}", order_id=f"{data[1]}", user_id=call.from_user.id)
            await call.answer(text = "Added to cart!", show_alert = True)
            datas = db.get_basket(user_id=call.from_user.id)
            total_price = 0
            text = "🛒 Basket\n\n"
            son = 0
            for datam in datas:
                son += 1
                for id in datam:
                    products = db.get_product(id=id)
                    narx = int(data[2]) * int(products[3])
                    total_price += narx
                    text += f"{son}. {products[1]}\n"
                    text += f"{data[2]} x {products[3]} = {float(narx)}CHF\n\n"
            text += f"Total: {float(total_price)}CHF"
            await call.message.answer(text = text,reply_markup = await check_of_order(order_id=f"{data[1]}"))
            await call.message.delete()
        else:
            try:
                db.add_basket(user_id=call.from_user.id, order_id=f"{data[1]}", number=f"{data[2]}")
                await call.answer(text = "Added to cart!", show_alert = True)
                datas = db.get_basket(user_id=call.from_user.id)
                total_price = 0
                text = "🛒 Basket\n\n"
                son = 0
                for datam in datas:
                    son += 1
                    for id in datam:
                        products = db.get_product(id=id)
                        narx = int(data[2]) * int(products[3])
                        total_price += narx
                        text += f"{son}. {products[1]}\n"
                        text += f"{data[2]} x {products[3]} = {float(narx)}CHF\n\n"
                text += f"Total: {float(total_price)}CHF"
                await call.message.answer(text = text, reply_markup = await check_of_order(order_id=f"{data[1]}"))
                await call.message.delete()
            except Exception as err:
                await call.message.answer(f"There was an error adding: {err}")
    except Exception as err:
        await call.message.answer(f"The error is gone: {err}")


# Savatga mahsulot qo'shish tugmasi uchun
@dp.callback_query_handler(text = "add")
async def back_sads(call: types.CallbackQuery):
    markup = await products_keyboard()
    await call.message.answer("Select a product", reply_markup=markup)
    await call.message.delete()

# Savatni tozalash tugmasi uchun handler
@dp.callback_query_handler(text="delete")
async def clear_basket_all(call: types.CallbackQuery):
    try:
        db.delete_basket(user_id=call.from_user.id)
        await call.message.answer("Select a product.", reply_markup=await products_keyboard())
        await call.message.delete()
    except Exception as err:
        await call.message.answer(f"Error: {err}")

# Savat ichidan orqaga qaytish uchun handler
@dp.callback_query_handler(text_contains = "somet:")
async def bassdffsd(call: types.CallbackQuery):
    id_product = call.data.replace("somet:", "")
    mahsulot = db.get_product(id = id_product)
    name = f"{mahsulot[1]}"
    rasm = mahsulot[2]
    narx = f"{mahsulot[3]}"
    text = f"🛍 <b>Name:</b> <i>{name}</i>\n"
    text += f"💸 <b>Price:</b> <i>{narx}</i>\n\n"
    text += f"<b>How many of this product would you like to order??</b>"
    markup = await numberorder(id=id_product, volume=1)
    await call.message.answer_photo(photo = rasm, caption=text, reply_markup=markup)
    await call.message.delete()

# Buyurtmani tasdiqlash tugmasi uchun
@dp.callback_query_handler(text_contains="tasdiq")
async def adsffdsa(call: types.CallbackQuery):
    await call.message.answer("Leave your phone number🔽:", reply_markup = contact)
    await call.message.delete()
    await Number_check.phone.set()

@dp.message_handler(state = Number_check.phone, content_types = 'contact')
async def get_phon(message: types.Message, state: FSMContext):
    num = message.contact.phone_number
    await state.update_data({
        "phone":num
        })
    dats = db.get_data_from_basket(user_id = message.from_user.id)
    son = 0
    total_price = 0
    text = ""
    for data in dats:
        son += 1
        mahsulot = db.get_product(id = data[0])
        narx = int(data[1])*int(mahsulot[3])
        total_price += narx
        text += f"{son}. {mahsulot[1]}\n"
        text += f"{data[1]} x {mahsulot[3]} = {narx} CHF\n\n"
    text += f"Total: {total_price}CHF\n"
    text += f"Phone number: {num}\n\n"
    text += f"<i>Will you order??</i>"
    await message.answer(text = text, reply_markup = yes_no)
    await message.delete()

# Foydalanuvchiga mahsulotlarni buyurtma berasizmi deganda ha ni bossa ishlaydigan handler
@dp.callback_query_handler(text="XA", state=Number_check.phone)
async def add_buasfdfasd(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        try:
            basket = db.datas_from_basket(user_id=call.from_user.id)
            db.add_order(user_id=call.from_user.id, status="waiting", phone=data.get('phone'))
            order_id = db.get_orders(user_id=call.from_user.id)[-1][0]
            for bas in basket:
                db.add_detials(order_id=order_id, book_id=bas[1], number=bas[2])
            db.delete_basket(user_id=call.from_user.id)
            text = "<i>🎉New order</i>\n"
            text += f"Order number: {order_id}\n\n"
            text += f"ID: {call.from_user.id}\n"
            text += f"Full name: {call.from_user.full_name}\n"
            text += f"Phone number: {data.get('phone')}\n"
            text += f"Username: @{call.from_user.username}\n\n"
            for admin in ADMINS:
                details = db.datas_detail(order_id=order_id)
                total_price = 0
                son = 0
                for detail in details:
                    product_id = detail[2]
                    number = detail[3]
                    nom = db.get_product(id=product_id)[1]
                    narx = db.get_product(id=product_id)[3]
                    price = number * narx
                    total_price += price
                    son += 1
                    text += f"{son}. 🛍 Product name: {nom}\n"
                    text += f"{number} x {narx} = {price} CHF\n"
                text += f"\nTotal price: {total_price} CHF"
                await bot.send_message(chat_id = admin, text = text, reply_markup = await acceptance(user_id = call.from_user.id, order_id = order_id))
            await call.answer("Sent to admin! ✅\nAdmins will contact you.", show_alert=True)
            await state.finish()
            await call.message.answer("<i>Main menu</i>", reply_markup=main)
            await call.message.delete()
        except Exception as err:
            await call.message.answer(f"The error is gone! {err}")
        await state.finish()
    except Exception as err:
        await call.message.answer(f"Error: {err}")

# Foydalanuvchiga shu mahsulotlarni buyurtma berasizmi deganda yo'q tugmasini bosganida ishlaydigan
@dp.callback_query_handler(text="YOQ", state=Number_check.phone)
async def add_buasfdfasd(call: types.CallbackQuery, state: FSMContext):
    try:
        db.delete_basket(user_id=call.from_user.id)
        await call.message.answer("❌ Canceled.", reply_markup=main)
        await call.message.delete()
        await state.finish()
    except Exception as err:
        await call.message.answer(f"Error: {err}")


# Admin shu foydalanuvchidan buyurtma kelganida qabul qilish tugmasini bossa ishlaydigan
@dp.callback_query_handler(text_contains = "accept")
async def accept_admin(call: types.CallbackQuery):
    data = call.data.rsplit(':')
    print(data)
    try:
        sana = db.get_data_order(user_id=data[1], order_id=data[2])
        if sana[2]!="accept":
            db.update_order_status(status="accept", user_id=data[1], order_id=data[2])
            text = "Your order has been accepted!✅\n"
            text += f"📅 The date: {sana[4]}\n\n"
            details = db.datas_detail(order_id=data[2])
            total_price = 0
            son = 0
            for detail in details:
                product_id = detail[2]
                number = detail[3]
                nom = db.get_product(id=product_id)[1]
                narx = db.get_product(id=product_id)[3]
                price = number * narx
                total_price += price
                son += 1
                text += f"{son}. 🛍 Product name: {nom}\n"
                text += f"{number} x {narx} = {price} CHF\n"
            text += f"\nTotal price: {total_price} CHF"
            await bot.send_message(chat_id=data[1], text = text)
            await call.answer("Accepted ✅", show_alert=True)
            text += "\nACCEPTED ✅"
            await call.message.answer(text=text)
            await call.message.delete()
        else:
            await call.answer("Previously accepted ✅", show_alert=True)
            await call.message.delete()
    except Exception as err:
        await bot.send_message(chat_id=917782961, text=f"ERROR: {err}")


# Admin shu foydalanuvchidan yangi buyurtma keldi deganida rad erish tugmasini bossa ishlaydigan handler
@dp.callback_query_handler(text_contains = "reject")
async def accept_admin(call: types.CallbackQuery):
    data = call.data.rsplit(':')
    print(data)
    try:
        sana = db.get_data_order(user_id=data[1], order_id=data[2])
        if sana[2] == "accept":
            await call.answer("Previously accepted ✅", show_alert=True)
            await call.message.delete()
        elif sana[2]!="reject":
            db.update_order_status(status="reject", user_id=data[1], order_id=data[2])
            text = "Canceled ❌\n"
            text += f"📅 Sana: {sana[4]}\n\n"
            details = db.datas_detail(order_id=data[2])
            total_price = 0
            son = 0
            for detail in details:
                product_id = detail[2]
                number = detail[3]
                nom = db.get_product(id=product_id)[1]
                narx = db.get_product(id=product_id)[3]
                price = number * narx
                total_price += price
                son += 1
                text += f"{son}. 🛍 Product name: {nom}\n"
                text += f"{number} x {narx} = {price} CHF\n"
            text += f"\nTotal price: {total_price} CHF"
            await bot.send_message(chat_id=data[1], text = text)
            await call.answer("Canceled ❌", show_alert=True)
            text += "\nCanceled ❌"
            await call.message.answer(text=text)
            await call.message.delete()
        else:
            await call.answer("Previously accepted ❌", show_alert=True)
            await call.message.delete()
    except Exception as err:
        await bot.send_message(chat_id=917782961, text=f"ERROR: {err}")

# Foydalanuvchi Mening buyurtmalarim tugmasini bossa ishlaydigan handler
@dp.message_handler(text = "📄 My orders")
async def nimadir(message: types.Message):
    if db.get_orders(user_id=message.from_user.id):
        datas = db.get_orders(user_id=message.from_user.id)
        for data in datas:
            print(data[4])
            text = ""
            id_order = data[0]
            text += f"🔢 Order id: {data[0]}\n"
            text += f"📆 To the date of the order: {data[4]}\n"
            if data[2]=="accept":
                text += "🟢 Order status: Accepted ✅\n\n"
            elif data[2] == "reject":
                text += "🔴 Order status: Rejected ❌\n\n"
            else:
                text += "🟣 Order status: Waiting ⏳\n\n"
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
                text += f"{number} x {product_price} = {price} CHF\n\n"
                total_price += price
            text += f"💸 Total: {total_price} CHF"
            await message.answer(text = text)
    else:
        await message.answer("🤷🏻‍♂️You have no orders.")