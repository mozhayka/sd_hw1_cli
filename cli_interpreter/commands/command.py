import sys
from abc import ABC, abstractmethod
from typing import TextIO


class Command(ABC):
    """
    Базовый класс команды, хранящий данные для выполнения команды
    """

    OK: int = 0
    ILLEGAL_ARGUMENT: int = 1
    DEFAULT_ERROR: int = 69

    def __init__(
            self,
            args: list[str] = None,
            input_stream: TextIO = None,
            output_stream: TextIO = None,
    ):
        """Конструктор класса команды
        :param args: список строк-аргументов команды
        :param input_stream: поток ввода
        :param output_stream: поток вывода
        """
        if args is None:
            args = []
        self.args = args
        self.input_stream = input_stream
        self.output_stream = output_stream

    @abstractmethod
    def execute(self) -> int:
        """
        Абстрактный метод, реализующий логику работы команды в наследнике
        @:return код ответа команды; 0 в случае успеха, иначе `int`
        """
        pass

    def __eq__(self, other):
        """
        Переопределенный метод сравнения двух экземпляров команд

        :param other: команда для сравнения
        :return: `True`, если тип и значения полей совпадают; иначе `False`
        """
        if type(self).__name__ != type(other).__name__:
            return False

        return (
                self.args == other.args
                and self.input_stream == other.input_stream
                and self.output_stream == other.output_stream
        )

    def __str__(self):
        """
        Переопределенный метод отображения состояния объекта в строку

        :return: строковое представление объекта
        """
        return f"{type(self).__name__}{self.__dict__}"

    def _write_output(self, output: str) -> None:
        """
        Выводит переданный текст в поток вывода

        :param output: выводимый текст
        """
        if not output.endswith("\n"):
            output += "\n"

        if self.output_stream:
            self.output_stream.write(output)
            self.output_stream.flush()
        else:
            sys.stdout.write(output)
            sys.stdout.flush()
