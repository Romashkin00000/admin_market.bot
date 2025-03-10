import logging
from telebot import TeleBot
import functions
import middlewares


class Bot:
    """Основной класс бота"""

    def __init__(self, env, db):
        """Инициализация бота"""
        token = env.get("TOKEN")
        self.env = env
        self.bot = TeleBot(token)
        self.db = db

        self.functions = []
        self.middlewares = []

        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.info("Бот успешно инициализирован")

    def run(self):
        """Запуск бота"""
        self._register_actions()
        self._register_middlewares()
        self.logger.info("Бот запущен")
        self.bot.polling()

    def _discover_middlewares(self):
        """Загрузка middleware"""
        for middleware in dir(middlewares):
            if middleware.startswith('_'):
                continue
            obj = getattr(middlewares, middleware)
            self.middlewares.append(obj)

    def _discover_functions(self):
        """Загрузка обработчиков"""
        for func in dir(functions):
            if func.startswith('_'):
                continue
            obj = getattr(functions, func)
            self.functions.append(obj)

    def _register_middlewares(self):
        """Регистрация middleware"""
        self._discover_middlewares()
        for middleware in self.middlewares:
            self.bot.add_middleware(middleware)
        self.logger.info(f"Зарегистрировано {len(self.middlewares)} middleware")

    def _register_actions(self):
        """Регистрация обработчиков сообщений и команд"""
        self._discover_functions()
        for klass in self.functions:
            routing_info = klass.info()

            trigger_info = routing_info[0]
            handler_info = routing_info[1]

            if trigger_info == "message":
                m_handler = self.bot.message_handler(**handler_info)
            elif trigger_info == "callback_query":
                m_handler = self.bot.callback_query_handler(**handler_info)
            elif trigger_info == "inline_query":
                m_handler = self.bot.inline_handler(**handler_info)

            m_handler(klass.init(env=self.env, bot=self.bot, db=self.db))

        self.logger.info(f"Зарегистрировано {len(self.functions)} обработчиков команд")