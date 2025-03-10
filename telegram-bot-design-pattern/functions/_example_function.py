from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """Создает главное меню с кнопками"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Показать товары", callback_data="show_products"))
    return markup
