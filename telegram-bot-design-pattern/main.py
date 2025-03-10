"""Bot start file"""
import os
from env import ENV
from core import Bot

try:
    from db import DB_CONNECTION
except ImportError:
    DB_CONNECTION = None

if __name__ == "__main__":
    bot = Bot(env=ENV, db=DB_CONNECTION)
    bot.run()