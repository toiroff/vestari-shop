from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    name = State()
    phone = State()

class edit_name(StatesGroup):
    name = State()

class edit_number(StatesGroup):
    phone = State()

class Number_check(StatesGroup):
    phone =State()
    check = State()

class Add_tarmoq (StatesGroup):
    name =State()
    url =State()

class Update_admin(StatesGroup):
    name = State()
    number = State()

class Category(StatesGroup):
    category = State()


class send_text(StatesGroup):
    name = State()

class send_photo(StatesGroup):
    name = State()

class send_doc(StatesGroup):
    name = State()

class send_video(StatesGroup):
    name = State()

class send_voice(StatesGroup):
    name = State()

class send_audio(StatesGroup):
    name = State()

class send_ctext(StatesGroup):
    name = State()

class send_caudio(StatesGroup):
    name = State()

class send_cvideo(StatesGroup):
    name = State()

class send_cdoc(StatesGroup):
    name = State()

class send_cvoice(StatesGroup):
    name = State()

class send_cphoto(StatesGroup):
    name = State()

class Add_products(StatesGroup):
    category = State()
    name = State()
    money = State()
    info = State()
    photo = State()
    check = State()

class Add_category(StatesGroup):
    name = State()
    check = State()


class Update_max_name(StatesGroup):
    name = State()

class Update_max_money(StatesGroup):
    name = State()

class Update_max_about(StatesGroup):
    name = State()

class Update_max_photo(StatesGroup):
    name = State()

class Update_category(StatesGroup):
    name = State()