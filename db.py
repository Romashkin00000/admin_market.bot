import psycopg2
from config import host, user, password, database
# Класс для работы с базой данных

class Database:
    def __init__(self, host, user, password, database):
        """ Инициализация и подключение к базе данных """
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def fetch_all_products(self):
        """ Получает все товары из таблицы """
        self.cursor.execute("SELECT id, title, is_active FROM таблица101")
        return self.cursor.fetchall()

    def update_product_status(self, product_id, is_active):
        """ Обновляет статус активности товара по ID """
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
        """ Закрывает соединение с базой данных """
        self.cursor.close()
        self.connection.close()
db = Database(host, user, password, database)

# Создаем экземпляр класса базы данных

