import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Показать товары", callback_data="show_products"))
    return markup
class CustomTeleBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
