import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

# ----------------- USERS TABLE -------------------
    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
        id	INTEGER NOT NULL UNIQUE,
        user_id	INTEGER NOT NULL,
        username TEXT,
        fullname TEXT,
        phone INTEGER NOT NULL,
        PRIMARY KEY(id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_all_message(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    # Foydalanuvchi qo'shish
    def add_user(self, user_id: int, username: str, fullname: str, phone: int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(user_id, username, fullname, phone) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, username, fullname, phone), commit=True)

    # Foydalanuvchini tekshirish bazada bor yoki yo'qligini
    def check_user(self, user_id):
        sql = f"""
         SELECT user_id FROM Users WHERE user_id=?
         """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    # Foydalanuvchining ismi va raqamini korish uchun
    def get_data_user(self, user_id):
        sql = f"""
         SELECT fullname, phone FROM Users WHERE user_id = ?
         """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    # Bazadagi foydalanuvchilarni soni
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_products(self):
        return self.execute("SELECT COUNT(*) FROM Products;", fetchall=True)

    # Foydalanuvchining ism fam taxrirlash
    def update_name(self, fullname, user_id):
        sql = f"""
        UPDATE Users SET fullname=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(fullname, user_id), commit=True)

    # Foydalanuvchining telning tahrirlash
    def update_phone(self, phone, user_id):
        sql = f"""
        UPDATE Users SET phone=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(phone, user_id), commit=True)

# --------------- MAHSULOTLAR TABLE -------------------
    def create_table_products(self):
        sql = """
        CREATE TABLE Products (
        	id	INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            product_photo TEXT NOT NULL,
            product_money INTEGER NOT NULL,
            product_about	TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)

    #Product buttonga chiqarish
    def get_products(self, category):
        sql = f"""
         SELECT * FROM Products WHERE product_category=?
         """
        return self.execute(sql, parameters=(category,), fetchall=True)

    def select_all_product(self):
        sql = """
        SELECT * FROM Products
        """
        return self.execute(sql, fetchall=True)

    def update_photo_max(self, product_photo, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET product_photo=? WHERE id=?
        """
        return self.execute(sql, parameters=(product_photo,id), commit=True)

    def update_category_max(self, category, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET product_category=? WHERE id=?
        """
        return self.execute(sql, parameters=(category,id), commit=True)

    def update_full_name_max(self, product_name, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET product_name=? WHERE id=?
        """
        return self.execute(sql, parameters=(product_name,id), commit=True)

    def update_money_max(self, product_money, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET product_money=? WHERE id=?
        """
        return self.execute(sql, parameters=(product_money,id), commit=True)

    def update_money_about(self, product_about, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET product_about=? WHERE id=?
        """
        return self.execute(sql, parameters=(product_about,id), commit=True)

    # Bazadan id orqali Product olish
    def get_product(self, id):
        sql = f"""
         SELECT * FROM Products WHERE id=?
         """
        return self.execute(sql, parameters=(id,), fetchone=True)

    # --------------- SAVAT TABLE -------------------
    def create_table_basket(self):
        sql = """
        CREATE TABLE Basket (
            user_id	INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            number INTEGER NOT NULL
            );
"""
        self.execute(sql, commit=True)

    # TEKSHIRISH BOR YOKI YOQLIGINI
    def check_order_id(self, order_id, user_id):
        sql = f"""
         SELECT order_id FROM Basket WHERE order_id=? AND user_id=?
         """
        return self.execute(sql, parameters=(order_id, user_id,), fetchall=True)

    # basket dagi numberni yangilash
    def update_number(self, number, order_id, user_id):
        sql = f"""
        UPDATE Basket SET number=? WHERE order_id=? AND user_id=?
        """
        return self.execute(sql, parameters=(number, order_id, user_id), commit=True)

    # Basktedan ma'lumotlarni olish
    def get_basket(self, user_id):
        sql = f"""
         SELECT order_id FROM Basket WHERE user_id=?
         """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    # Basketga qo'shish
    def add_basket(self, user_id: int, order_id:int, number:int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
          INSERT INTO Basket(user_id, order_id, number) VALUES(?, ?, ?)
          """
        self.execute(sql, parameters=(user_id, order_id, number), commit=True)

    # Savatni tozalash
    def delete_basket(self,user_id):
        sql = f"""
        DELETE FROM Basket WHERE user_id=?
        """
        return self.execute(sql, parameters=(user_id,), commit=True)

    def get_data_from_basket(self, user_id):
        sql = f"""
         SELECT order_id, number FROM Basket WHERE user_id=?
         """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def datas_from_basket(self, user_id):
        sql = f"""
         SELECT * FROM Basket WHERE user_id=?
         """
        return self.execute(sql, parameters=(user_id,), fetchall=True)



    # --------------- ORDERS TABLE -------------------
    def create_table_orders(self):
        sql = """
        CREATE TABLE Orders (
           	order_id	INTEGER NOT NULL UNIQUE,
            user_id	INTEGER NOT NULL,
            status	TEXT NOT NULL,
            phone	INTEGER NOT NULL,
            created_time	DATETIME DEFAULT ((DATETIME('now', 'localtime'))),
            PRIMARY KEY(order_id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)



    # Ordersga qo'shish
    def add_order(self, user_id: int, status:int, phone:int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
          INSERT INTO Orders(user_id, status, phone) VALUES(?, ?, ?)
          """
        self.execute(sql, parameters=(user_id, status, phone), commit=True)

    # Orders dan hamma orderlarni olish
    def get_orders(self, user_id):
        sql = f"""
         SELECT * FROM Orders WHERE user_id=?
         """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    # --------------- DETIALS TABLE -------------------
    def create_table_detials(self):
        sql = """
        CREATE TABLE Order_detials (
            id INTEGER NOT NULL UNIQUE,
            order_id TEXT NOT NULL,
            book_id	INTEGER NOT NULL,
            number INTEGER NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)

    # Ordersga qo'shish
    def add_detials(self, order_id: int, book_id: int, number: int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
          INSERT INTO Order_detials(order_id, book_id, number) VALUES(?, ?, ?)
          """
        self.execute(sql, parameters=(order_id, book_id, number), commit=True)


    def datas_detail(self, order_id):
        sql = f"""
         SELECT * FROM Order_detials WHERE order_id=?
         """
        return self.execute(sql, parameters=(order_id,), fetchall=True)

    def get_data_order(self, user_id, order_id):
        sql = f"""
         SELECT * FROM Orders WHERE user_id=? AND order_id=?
         """
        return self.execute(sql, parameters=(user_id,order_id,), fetchone=True)

    def update_order_status(self, status, user_id, order_id):
        sql = f"""
        UPDATE Orders SET status=? WHERE user_id=? AND order_id=?
        """
        return self.execute(sql, parameters=(status, user_id, order_id), commit=True)

    # --------------- TARMOQLAR TABLE -------------------
    def create_table_Messages(self):
        sql = """
        CREATE TABLE Messages (
        id	INTEGER NOT NULL UNIQUE,
        name TEXT,
        url TEXT,
        PRIMARY KEY(id AUTOINCREMENT)
            );
    """
        self.execute(sql, commit=True)

    def delete_tarmoq_admin(self,order_id):
        self.execute(f"DELETE FROM Messages WHERE id={order_id}", commit=True)

    def add_tarmoq(self,name:str, url:str):
        # SQL_EXAMPLE ="INSERT INTO myfiles_teacher(id,name,email)VALUES(1,"john","john@hgmail.com")"

        sql="""
        INSERT INTO Messages (name, url) VALUES(?,?)
        """
        self.execute(sql, parameters=(name, url), commit=True)


    def select_all_tarmoq(self):
        sql = """
        SELECT * FROM Messages
        """
        return self.execute(sql, fetchall=True)

        # --------------- TARMOQLAR TABLE -------------------

    def create_table_call(self):
        sql = """
          CREATE TABLE Call (
          id	INTEGER NOT NULL UNIQUE,
          number INTEGER,
          url TEXT,
          user_id INTEGER NOT NULL UNIQUE,
          PRIMARY KEY(id AUTOINCREMENT)
              );
      """
        self.execute(sql, commit=True)


    def add_message(self,user_id:int, number: int=None, url:str=None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
          INSERT INTO Call(user_id, number, url) VALUES(?, ?, ?)
          """
        self.execute(sql, parameters=(user_id, number, url), commit=True)


    def update_full_name_admin(self, url, user_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Call SET url=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(url,user_id), commit=True)

    def update_full_number_admin(self, number, user_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Call SET number=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(number,user_id), commit=True)

    def select_all_admin(self):
        sql = """
        SELECT * FROM Call
        """
        return self.execute(sql, fetchall=True)








    def create_table_qator(self):
        sql = """
          CREATE TABLE Tab_order (
          id	INTEGER NOT NULL UNIQUE,
          number INTEGER,
          PRIMARY KEY(id AUTOINCREMENT)
              );
      """
        self.execute(sql, commit=True)


    def update_qator(self,  number,):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Tab_order SET number=? WHERE id=1
        """
        return self.execute(sql, parameters=(number,), commit=True)

    def select_menu(self):
        sql = """
        SELECT * FROM Tab_order
        """
        return self.execute(sql, fetchall=True)

    def status_orders(self, status):
        sql = f"""
         SELECT * FROM Orders WHERE status=?
         """
        return self.execute(sql, parameters=(status,), fetchall=True)


    def add_products(self, product_name: str, product_photo: str, product_money: int, product_about: str,
                     product_category: str):
        sql = """
        INSERT INTO Products (product_name, product_photo, product_money, product_about, product_category)
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(product_name, product_photo, product_money, product_about, product_category),
                     commit=True)

    def delete_order_admin(self, order_id):
        self.execute(f"DELETE FROM Products WHERE id={order_id}", commit=True)

    def delete_order(self, order_id):
        self.execute(f"DELETE FROM Orders WHERE order_id={order_id}", commit=True)

    def delete_order_details(self, order_id):
            self.execute(f"DELETE FROM Order_detials WHERE order_id={order_id}", commit=True)

    def delete_category(self, id):
        self.execute(f"DELETE FROM Category WHERE id={id}", commit=True)

    def select_all_products(self):
        sql = """
        SELECT * FROM Products
        """
        return self.execute(sql, fetchall=True)

    def get_category(self):
        sql = """
         SELECT * FROM Category
         """
        return self.execute(sql, fetchall=True)

    def add_category(self,name:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Category(Category) VALUES(?)
        """
        self.execute(sql, parameters=(name,), commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")