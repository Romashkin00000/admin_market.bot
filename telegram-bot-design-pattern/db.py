import psycopg2
from env import ENV

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=ENV["DB_HOST"],
            user=ENV["DB_USER"],
            password=ENV["DB_PASSWORD"],
            database=ENV["DB_NAME"]
        )
        self.cursor = self.connection.cursor()

    def fetch_all_products(self):
        self.cursor.execute("SELECT id, title, is_active FROM таблица101")
        return self.cursor.fetchall()

    def update_product_status(self, product_id, is_active):
        self.cursor.execute("""
            UPDATE таблица101
            SET is_active = %s
            WHERE id = %s
            RETURNING id, title, is_active;
        """, (is_active, product_id))
        updated_product = self.cursor.fetchone()
        self.connection.commit()
        return updated_product

    def close(self):
        self.cursor.close()
        self.connection.close()

DB_CONNECTION = Database()