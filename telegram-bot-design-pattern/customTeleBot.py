import telebot

class TeleBot(telebot.TeleBot):
    """Custom TeleBot class"""

    # Список для хранения middleware
    middlewares = []

    def __init__(self, token):
        super().__init__(token)

    # Функция для добавления middleware
    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    # Переопределяем метод для обработки команд
    def _notify_command_handlers(self, handlers, new_messages):
        for message in new_messages:
            # Сначала обрабатываем сообщение через все middleware
            for middleware in self.middlewares:
                message = middleware.init(message)

            # Если сообщение не должно обрабатываться дальше, пропускаем его
            if hasattr(message, 'chat') and message.chat and (message.chat.id in self.message_subscribers_next_step):
                continue

            # Проверяем и вызываем соответствующие обработчики
            for message_handler in handlers:
                if self._test_message_handler(message_handler, message):
                    self._exec_task(message_handler['function'], message)
                    break