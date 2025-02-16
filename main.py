# main.py
from markTelegram import bot
import telebot
from db import db

# Запуск бота
if __name__ == "__main__":
    bot.polling()
