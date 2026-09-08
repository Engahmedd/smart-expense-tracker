class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def check_password(self, password):
        return self.password == password

    def save(self, database):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        values = (self.username, self.password)
        database.execute_query(query, values)
        print("User saved successfully!")

    @staticmethod
    def login(database, username, password):
        query = "SELECT * FROM users WHERE username = ?"
        result = database.fetch_one(query, (username,))

        if result is None:
            print("User not found")
            return None

        # تحويل sqlite3.Row إلى قراءة مباشرة لحقول الجدول
        user = User(
            id=result['id'], 
            username=result['username'], 
            email="", # تم ترك الإيميل فارغ لعدم وجوده بالداتا بيز
            password=result['password']
        )

        if user.check_password(password):
            print("Login successful!")
            return user
        else:
            print("Wrong password")
            return None


class Transaction:
    def __init__(self, user_id, amount, category, trans_type, date, note="", trans_id=None):
        self.id = trans_id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.type = trans_type
        self.date = date
        self.note = note

    def save(self, database):
        query = "INSERT INTO transactions (user_id, amount, category, type, date) VALUES (?, ?, ?, ?, ?)"
        values = (self.user_id, self.amount, self.category, self.type, self.date)
        database.execute_query(query, values)
        print("Transaction saved successfully!")

    @staticmethod
    def get_user_transactions(database, user_id):
        query = "SELECT id, amount, category, type, date FROM transactions WHERE user_id = ? ORDER BY date DESC"
        return database.fetch_all(query, (user_id,))


class Budget:
    def __init__(self, user_id, category, monthly_limit, budget_id=None):
        self.id = budget_id
        self.user_id = user_id
        self.category = category
        self.monthly_limit = monthly_limit

    def save(self, database):
        query = "INSERT INTO budgets (user_id, category, budget_limit) VALUES (?, ?, ?)"
        values = (self.user_id, self.category, self.monthly_limit)
        database.execute_query(query, values)
        print("Budget saved successfully!")

    @staticmethod
    def check_status(database, user_id, category, current_spending):
        query = "SELECT budget_limit FROM budgets WHERE user_id = ? AND category = ?"
        result = database.fetch_one(query, (user_id, category))
        
        if not result:
            return "No budget set for this category"
        
        limit = result['budget_limit']
        if current_spending > limit:
            return f"Over Budget! (Exceeded by {current_spending - limit})"
        else:
            return f"Within Limit (Remaining: {limit - current_spending})"
