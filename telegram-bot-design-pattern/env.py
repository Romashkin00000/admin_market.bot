
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Словарь с переменными окружения
ENV = {
    "TOKEN": os.getenv("TOKEN"),
    "ID_ADMIN": int(os.getenv("ID_ADMIN", 0)),  # ID админа
    "DB_HOST": os.getenv("HOST"),
    "DB_USER": os.getenv("USER"),
    "DB_PASSWORD": os.getenv("PASSWORD"),
    "DB_NAME": os.getenv("DATABASE"),
}