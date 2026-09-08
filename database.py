import sqlite3

class Database:
    def __init__(self, db_name="expense_tracker.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        # الاتصال بملف قاعدة البيانات المحلي
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # عشان نرجّع النتائج كـ Dictionary
        return conn

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # جدول المستخدمين
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # جدول المعاملات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # جدول الميزانية
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT NOT NULL,
                budget_limit REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        conn.commit()
        conn.close()