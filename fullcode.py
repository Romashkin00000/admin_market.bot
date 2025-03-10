import telebot
import psycopg2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import host, user, password, database
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('telethon')

# Telegram Bot Token
TOKEN = '7853003755:AAEE6Nh6_dZg_Izze1-UscLI8-CnAd6r5k8'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения статуса авторизации пользователей
user_auth_status = {}

# Пароль для авторизации
idadmin = 1075470938



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


# Создаем экземпляр класса базы данных
db = Database(host, user, password, database)


# Главное меню с кнопками
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Показать товары", callback_data="show_products"))
    return markup


# Кнопка "Главное меню"
def back_to_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Вернуться в меню", callback_data="main_menu"))
    return markup


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != idadmin:
        bot.send_message(message.chat.id, "⛔️ Доступ запрещен!")
        return

    bot.send_message(message.chat.id, "👋 Привет! Выберите действие:", reply_markup=main_menu())

# Отображение списка товаров с кнопками "Активировать" / "Деактивировать"
@bot.callback_query_handler(func=lambda call: call.data == "show_products")
def show_products(call):
    if call.message.chat.id != idadmin:
        bot.send_message(call.message.chat.id, "⛔️ Доступ запрещен!")
        return

    products = db.fetch_all_products()

    if not products:
        bot.send_message(call.message.chat.id, "Нет доступных товаров.", reply_markup=back_to_menu())
        return

    for product in products:
        product_id, title, is_active = product
        status_text = "✅ Активен" if is_active else "❌ Неактивен"

        # Создаем кнопки для изменения статуса
        markup = InlineKeyboardMarkup()
        if is_active:
            markup.add(InlineKeyboardButton("❌ Деактивировать", callback_data=f"toggle_{product_id}_0"))
        else:
            markup.add(InlineKeyboardButton("✅ Активировать", callback_data=f"toggle_{product_id}_1"))

        bot.send_message(call.message.chat.id, f"🆔 ID: {product_id}\n📦 Товар: {title}\n📌 Статус: {status_text}",
                         reply_markup=markup)

    bot.send_message(call.message.chat.id, "Выберите товар для изменения статуса:", reply_markup=back_to_menu())


@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def toggle_status(call):
    if call.message.chat.id != idadmin:
        bot.send_message(call.message.chat.id, "⛔️ Доступ запрещен!")
        return

    _, product_id, new_status = call.data.split("_")
    product_id = int(product_id)
    is_active = bool(int(new_status))

    updated_product = db.update_product_status(product_id, is_active)

    if updated_product:
        prod_id, title, new_status = updated_product
        status_text = "✅ Активен" if new_status else "❌ Неактивен"
        bot.edit_message_text(f"🆔 ID: {prod_id}\n📦 Товар: {title}\n📌 Статус: {status_text}",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=None)
        bot.answer_callback_query(call.id, "Статус товара обновлен! ✅")
    else:
        bot.answer_callback_query(call.id, "Ошибка! Товар не найден.", show_alert=True)


# Обработка нажатия "Главное меню"
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def go_main_menu(call):
    if call.message.chat.id != idadmin:
        bot.send_message(call.message.chat.id, "⛔️ Доступ запрещен!")
        return

    bot.send_message(call.message.chat.id, "🔝 Главное меню:", reply_markup=main_menu())


# Запуск бота
bot.polling()