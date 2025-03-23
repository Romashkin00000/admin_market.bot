from customTeleBot import main_menu  # Импортируем main_menu
def check_auth(bot, admin_id):
    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.id != admin_id:
            bot.send_message(message.chat.id, "⛔️ Доступ запрещен!")
            return
        bot.send_message(message.chat.id, "👋 Привет! Выберите действие:", reply_markup=main_menu())
