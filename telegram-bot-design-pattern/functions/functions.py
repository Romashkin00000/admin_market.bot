from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Показать товары", callback_data="show_products"))
    return markup

def back_to_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Вернуться в меню", callback_data="main_menu"))
    return markup

def setup_handlers(bot, db):
    @bot.callback_query_handler(func=lambda call: call.data == "show_products")
    def show_products(call):
        products = db.fetch_all_products()
        if not products:
            bot.send_message(call.message.chat.id, "Нет доступных товаров.", reply_markup=back_to_menu())
            return
        for product_id, title, is_active in products:
            status_text = "✅ Активен" if is_active else "❌ Неактивен"
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "❌ Деактивировать" if is_active else "✅ Активировать",
                    callback_data=f"toggle_{product_id}_{int(not is_active)}"
                )
            )
            bot.send_message(call.message.chat.id, f"🆔 ID: {product_id}\n📦 Товар: {title}\n📌 Статус: {status_text}",
                             reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
    def toggle_status(call):
        _, product_id, new_status = call.data.split("_")
        updated_product = db.update_product_status(int(product_id), bool(int(new_status)))

        if updated_product:
            prod_id, title, new_status = updated_product
            status_text = "✅ Активен" if new_status else "❌ Неактивен"
            bot.edit_message_text(f"🆔 ID: {prod_id}\n📦 Товар: {title}\n📌 Статус: {status_text}",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Статус товара обновлен! ✅")
        else:
            bot.answer_callback_query(call.id, "Ошибка! Товар не найден.", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def go_main_menu(call):
        bot.send_message(call.message.chat.id, "🔝 Главное меню:", reply_markup=main_menu())