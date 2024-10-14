import os
import re


class CliContext:

    def __init__(self):
        self.env: dict[str, str] = dict(os.environ)

    @staticmethod
    def _is_valid_variable_name(variable: str):
        return re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", variable) is not None

    def get(self, variable: str) -> str:
        """
        Возвращает значение переменной окружения.
        :param variable: Название переменной окружения
        :return: Значение переменной окружения, если такая есть в контексте; иначе возвращает пустую строку
        """
        return self.env.get(variable, "")

    def set(self, variable: str, value: str) -> None:
        """
        Сохраняет значение переменной окружения.
        Если такая переменная отсутствует, то создаст новое вхождение в словаре `env`,
        иначе обновит старое значение новым
        :param variable: Название переменной окружения
        :param value: Значение переменной окружения
        """
        if not self._is_valid_variable_name(variable):
            raise ValueError(f"Invalid environment variable name: '{variable}'")
        self.env[variable] = value
