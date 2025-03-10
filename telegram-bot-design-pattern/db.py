#from db import db
import psycopg2
import logging
from env import ENV

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        """ Инициализация и подключение к базе данных """
        try:
            self.connection = psycopg2.connect(
                host=ENV["HOST"],
                user=ENV["USER"],
                password=ENV["PASSWORD"],
                database=ENV["DATABASE"]
            )
            self.cursor = self.connection.cursor()
            logger.info("Успешное подключение к базе данных")
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def fetch_all_products(self):
        """ Получает все товары из таблицы """
        try:
            self.cursor.execute("SELECT id, title, is_active FROM таблица101")
            products = self.cursor.fetchall()
            logger.info(f"Получено {len(products)} товаров из базы данных")
            return products
        except Exception as e:
            logger.error(f"Ошибка при получении товаров: {e}")
            return []

    def update_product_status(self, product_id, is_active):
        """ Обновляет статус активности товара по ID """
        try:
            self.cursor.execute("""
                UPDATE таблица101
                SET is_active = %s
                WHERE id = %s
                RETURNING id, title, is_active;
            """, (is_active, product_id))
            updated_product = self.cursor.fetchone()
            self.connection.commit()

            if updated_product:
                logger.info(
                    f"Обновлен статус товара: ID {updated_product[0]}, Статус {'Активен' if updated_product[2] else 'Неактивен'}")
            else:
                logger.warning(f"Товар с ID {product_id} не найден")

            return updated_product
        except Exception as e:
            logger.error(f"Ошибка при обновлении статуса товара: {e}")
            return None

    def close(self):
        """ Закрывает соединение с базой данных """
        try:
            self.cursor.close()
            self.connection.close()
            logger.info("Соединение с базой данных закрыто")
        except Exception as e:
            logger.error(f"Ошибка при закрытии соединения: {e}")


# Создаем экземпляр класса базы данных
db = Database()
