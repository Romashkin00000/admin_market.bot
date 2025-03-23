from customTeleBot import CustomTeleBot
from middleware import check_auth
from functions import setup_handlers

class Bot:
    def __init__(self, env, db):
        self.env = env
        self.db = db
        self.bot = CustomTeleBot(env["TOKEN"])

    def run(self):
        check_auth(self.bot, self.env["ID_ADMIN"])
        setup_handlers(self.bot, self.db)
        self.bot.polling()
