from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from loader import db

panel = InlineKeyboardMarkup(
	inline_keyboard = [
		[
			InlineKeyboardButton(text = "🛍 Orders", callback_data = 'orders'),
			InlineKeyboardButton(text = "🤖 Edit bot", callback_data = "edit_bot"),
		],
		[
			InlineKeyboardButton(text = "📊 Users", callback_data = "statistics"),
			InlineKeyboardButton(text = "🗄 Download base", callback_data = "download_base")
		],
		[
			InlineKeyboardButton(text = "📝 Send a post", callback_data="send_post")
		],
		[
			InlineKeyboardButton(text = "❌ Close panel", callback_data = "close_panel")
		]
	]
)



edit_bot = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text = "🛍 Edit products", callback_data = "edit_products"),
			InlineKeyboardButton(text = "🛠 Product line", callback_data="edit_qator")
		],
		[
			InlineKeyboardButton(text = "📞 Edit Contact Us", callback_data="aloqa"),
			InlineKeyboardButton(text = "🔵 Edit social networks", callback_data="edit_mes"),
		],
		[
			InlineKeyboardButton(text = "↪️ Back", callback_data="back_to_panel"),
			InlineKeyboardButton(text = "❌ Close panel", callback_data = "close_panel")
		]
	]
)

orders_btns = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text = "✅ Confirmed", callback_data="accepted"),
			InlineKeyboardButton(text = "❌ Rejected", callback_data="rejected")
		],
		[
			InlineKeyboardButton(text = "⏳ Waiting", callback_data="waiting")
		],
		[
			InlineKeyboardButton(text = "↪️ Back", callback_data="back_to_panel"),
			InlineKeyboardButton(text = "❌ Clos panel", callback_data="close_panel")
		]
	]
)

base_download = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text = "📃 Upload in Excel format", callback_data="type_excel"),
			InlineKeyboardButton(text = "🗄 Loading the database file itself", callback_data="type_db"),
		],
		[
			InlineKeyboardButton(text = "↪️ Back", callback_data="back_to_panel"),
			InlineKeyboardButton(text = "❌ Close panel", callback_data = "close_panel"),
		]
	]
)


orders_btns = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text = "✅ Confirmed", callback_data="accepted"),
			InlineKeyboardButton(text = "❌ Rejected", callback_data="rejected")
		],
		[
			InlineKeyboardButton(text = "⏳ Waiting", callback_data="waiting")
		],
		[
			InlineKeyboardButton(text = "↪️ Back", callback_data="back_to_panel"),
			InlineKeyboardButton(text = "❌ Close panel", callback_data="close_panel")
		]
	]
)



add_tarmoq_buttons = InlineKeyboardMarkup(
	inline_keyboard = [
		[
			InlineKeyboardButton(text = "Add", callback_data = "add_tarmoq_to_base"),
			InlineKeyboardButton(text = "Cancel", callback_data = "cancel_tarmoq"),
		]
	]
)


cancedsfasdfds = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text = "❌ Cancel", callback_data="bekorqilishpost")
		]
	]
)

class Keyboards:
	def messages(self):
		menu = InlineKeyboardMarkup(row_width=1)
		Shops_plus = InlineKeyboardButton("🔵 Add network", callback_data="Tarmoq_add")
		shops_del = InlineKeyboardButton("🗑 Delete network", callback_data="Tarmoq_del")
		back = InlineKeyboardButton("◀️ Back", callback_data="back_to_panel")
		exit = InlineKeyboardButton("Close panel", callback_data = "close_panel")
		return menu.add(Shops_plus, shops_del, back,exit)

	def admin_aloqa(self):
		menu = InlineKeyboardMarkup(row_width=1)
		Shops_plus = InlineKeyboardButton("📝 Edit Online Admin", callback_data=f"Admin_edit")
		shops_del = InlineKeyboardButton("📝 Edit phone number", callback_data="admin_number_edit")
		back = InlineKeyboardButton("◀️ Back", callback_data="back_to_panel")
		return menu.add(Shops_plus, shops_del, back)

	def contact(self):
		menu = ReplyKeyboardMarkup(resize_keyboard=True)
		contact = KeyboardButton("Send a number 📞", request_contact=True)
		return menu.add(contact)


	def admin_send_all(self):
		menu = InlineKeyboardMarkup(row_width=3)
		bir = InlineKeyboardButton("1", callback_data=f"bir_send")
		ikki = InlineKeyboardButton("2", callback_data="ikki_send")
		uch = InlineKeyboardButton("3", callback_data="uch_send")
		back = InlineKeyboardButton("◀️ Back", callback_data="back_to_panel")
		return menu.add(bir, ikki, uch, back)


	def admin_send_forward(self):
		menu = InlineKeyboardMarkup(row_width=3)
		bir = InlineKeyboardButton("1", callback_data=f"bir_sendf")
		ikki = InlineKeyboardButton("2", callback_data="ikki_sendf")
		uch = InlineKeyboardButton("3", callback_data="uch_sendf")
		tort = InlineKeyboardButton("4", callback_data=f"tort_sendf")
		besh = InlineKeyboardButton("5", callback_data="besh_sendf")
		olt = InlineKeyboardButton("6", callback_data="olt_sendf")
		back = InlineKeyboardButton("◀️ Back", callback_data="backadmf")
		return menu.add(bir, ikki, uch, tort, besh, olt, back)


	def admin_send_copy(self):
		menu = InlineKeyboardMarkup(row_width=3)
		bir = InlineKeyboardButton("1", callback_data=f"bir_sendc")
		ikki = InlineKeyboardButton("2", callback_data="ikki_sendc")
		uch = InlineKeyboardButton("3", callback_data="uch_sendc")
		tort = InlineKeyboardButton("4", callback_data=f"tort_sendc")
		besh = InlineKeyboardButton("5", callback_data="besh_sendc")
		olt = InlineKeyboardButton("6", callback_data="olt_sendc")
		back = InlineKeyboardButton("◀️ Orqaga", callback_data="backadmf")
		return menu.add(bir, ikki, uch, tort, besh, olt, back)


	def admin_send_bot(self):
		menu = InlineKeyboardMarkup(row_width=3)
		bir = InlineKeyboardButton("1", callback_data=f"bir_sendb")
		ikki = InlineKeyboardButton("2", callback_data="ikki_sendb")
		uch = InlineKeyboardButton("3", callback_data="uch_sendb")
		tort = InlineKeyboardButton("4", callback_data=f"tort_sendb")
		besh = InlineKeyboardButton("5", callback_data="besh_sendb")
		olt = InlineKeyboardButton("6", callback_data="olt_sendb")
		back = InlineKeyboardButton("◀️ Orqaga", callback_data="backadmf")
		return menu.add(bir, ikki, uch, tort, besh, olt, back)

	def check(self):
		menu = InlineKeyboardMarkup(row_width=1)
		Shops_plus = InlineKeyboardButton("✅ Yes", callback_data="check_mah")
		shops_del = InlineKeyboardButton("❌ No", callback_data="off_mah")
		return menu.add(Shops_plus, shops_del)

	def shop(self):
		menu = InlineKeyboardMarkup(row_width=2)
		Shops_plus = InlineKeyboardButton("🛍 Add product", callback_data="Mahsulot_add")
		Shops_category = InlineKeyboardButton("🛍 Add Category", callback_data="category_add")
		category_del = InlineKeyboardButton("🗑 Delete category", callback_data="category_del")
		shops_del = InlineKeyboardButton("🗑 Delete product", callback_data="Mahsulot_del")
		shops_edit = InlineKeyboardButton("📝 Edit product", callback_data="Mahsulot_edit")
		back = InlineKeyboardButton("◀️ Back", callback_data="back_to_panel")
		return menu.add(Shops_plus,Shops_category,shops_del,category_del,  shops_edit, back,)

kb =Keyboards()

async def delete_tarmoq_admin():

    markup = InlineKeyboardMarkup(row_width=1)
    products= db.select_all_tarmoq()
    for x in products:
        button_text = x[1]
        callback_data = f"admin_del_tarmoq:{x[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=callback_data)
                      )
    markup.insert(
            InlineKeyboardButton("◀️ Back",callback_data="back_to_panel")
        )
    return markup

async def delete_products_admin():
    g =db.select_menu()
    for i in g:
        raqam = int(f"{i[1]}")
        markup = InlineKeyboardMarkup(row_width=raqam)
    products= db.select_all_products()
    for x in products:
        button_text = x[1]
        callback_data = f"admin_del_products:{x[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=callback_data)
                      )
    markup.insert(
            InlineKeyboardButton("◀️ back",callback_data="back_to_panel")
        )
    return markup

async def delete_category_admin():
    # g =db.select_menu()
    # for i in g:
    #     raqam = int(f"{i[1]}")
    markup = InlineKeyboardMarkup(row_width=2)
    products= db.get_category()
    for x in products:
        button_text = x[1]
        callback_data = f"admin_del_category:{x[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=callback_data)
                      )
    markup.insert(
            InlineKeyboardButton("◀️ back",callback_data="back_to_panel")
        )
    return markup

async def select_category_admin():
    # g =db.select_menu()
    # for i in g:
    #     raqam = int(f"{i[1]}")
    markup = InlineKeyboardMarkup(row_width=2)
    products= db.get_category()
    for x in products:
        button_text = x[1]
        callback_data = f"admin_del_category:{x[1]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=button_text)
                      )

    return markup




async def edit_products_admin():
    g =db.select_menu()
    for i in g:
        raqam = int(f"{i[1]}")
        markup = InlineKeyboardMarkup(row_width=raqam)
    products= db.select_all_products()
    for x in products:
        button_text = x[1]
        callback_data = f"admin_edit_products:{x[0]}"

        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=callback_data)
                      )
    markup.insert(
            InlineKeyboardButton("◀️ Back",callback_data="back_to_panel")
        )
    return markup

async def EDIT_maxsulot(order_id):
    markup = InlineKeyboardMarkup(row_width=2).add(
				InlineKeyboardButton(text="📝 Category", callback_data=f"ctg_edt:{order_id}"),
                InlineKeyboardButton(text="📝 Name",callback_data=f"name_edt:{order_id}"),
                InlineKeyboardButton(text="📝 Price", callback_data=f"money_edt:{order_id}"),
                InlineKeyboardButton(text="📝 Photo",callback_data=f"photo_edt:{order_id}"),
				InlineKeyboardButton(text="📝 About", callback_data=f"about_edt:{order_id}"),
                InlineKeyboardButton(text="◀Back",callback_data=f"back_to_panel"))

    return markup
