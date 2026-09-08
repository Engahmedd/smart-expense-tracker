class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def check_password(self, password):
        return self.password == password

    def save(self, database):
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (self.username, self.email, self.password)
        database.execute_query(query, values)
        print("User saved successfully!")

    @staticmethod
    def login(database, username, password):
        query = "SELECT * FROM users WHERE username = %s"
        result = database.fetch_one(query, (username,))

        if result is None:
            print("User not found")
            return None

        user = User(result[0], result[1], result[2], result[3])

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
        query = "INSERT INTO transactions (user_id, amount, category, type, date, note) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.user_id, self.amount, self.category, self.type, self.date, self.note)
        database.execute_query(query, values)
        print("Transaction saved successfully!")

    @staticmethod
    def get_user_transactions(database, user_id):
        query = "SELECT id, amount, category, type, date, note FROM transactions WHERE user_id = %s ORDER BY date DESC"
        return database.fetch_all(query, (user_id,))


class Budget:
    def __init__(self, user_id, category, monthly_limit, budget_id=None):
        self.id = budget_id
        self.user_id = user_id
        self.category = category
        self.monthly_limit = monthly_limit

    def save(self, database):
        query = "INSERT INTO budgets (user_id, category, monthly_limit) VALUES (%s, %s, %s)"
        values = (self.user_id, self.category, self.monthly_limit)
        database.execute_query(query, values)
        print("Budget saved successfully!")

    @staticmethod
    def check_status(database, user_id, category, current_spending):
        query = "SELECT monthly_limit FROM budgets WHERE user_id = %s AND category = %s"
        result = database.fetch_one(query, (user_id, category))
        
        if not result:
            return "No budget set for this category"
        
        limit = result[0]
        if current_spending > limit:
            return f"Over Budget! (Exceeded by {current_spending - limit})"
        else:
            return f"Within Limit (Remaining: {limit - current_spending})"