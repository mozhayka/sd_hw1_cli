from typing import Dict


class CliContext:

    def __init__(self):
        self.env: Dict[str, str] = dict()  # TODO: попробовать сделать импорт переменных окружения текущего пользователя

    def get(self, variable: str) -> str:
        """
        Возвращает значение переменной окружения.
        :param variable: Название переменной окружения
        :return: Значение переменной окружения, если такая есть в контексте; иначе возвращает пустую строку
        """
        if variable in self.env:
            return self.env[variable]

        return ''

    def set(self, variable: str, value: str) -> None:
        """
        Сохраняет значение переменной окружения.
        Если такая переменная отсутствует, то создаст новое вхождение в словаре `env`,
        иначе обновит старое значение новым
        :param variable: Название переменной окружения
        :param value: Значение переменной окружения
        """
        self.env[variable] = value
