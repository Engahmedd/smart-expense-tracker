import mysql.connector 
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ahmedsameh0.0.2",
        database="expense_tracker"
    )
        self.cursor = self.conn.cursor()
        print("connected successfully")


    def create_tables(self):
        self.cursor.execute ("""CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100),
            password VARCHAR(255) NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10, 2),
            category VARCHAR(50),
            type VARCHAR(50),
            date DATE,
            note VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            category VARCHAR(50),
            monthly_limit DECIMAL(10, 2),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        self.conn.commit()
        print("Tables created successfully!")

if __name__ == "__main__":
    db = Database()
    db.create_tables()