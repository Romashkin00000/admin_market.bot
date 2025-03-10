class ExampleMiddleware:
    """Пример middleware для обработки сообщений"""

    def __init__(self, message):
        self.message = message

    @classmethod
    def init(cls, message):
        instance = cls(message)
        return instance.main(message)

    def main(self, message):
        """Функция обработки сообщений"""
        print(f"Сообщение '{message.text}' обработано в {self.__class__.__name__}!")

        return message  # Возвращаем сообщение без изменений