import sys
from abc import ABC, abstractmethod
from typing import TextIO


class Command(ABC):
    """
    Базовый класс команды, хранящий данные для выполнения команды
    """

    def __init__(self,
                 args: list[str] = None,
                 input_stream: TextIO = None,
                 output_stream: TextIO = None):
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
    def execute(self):
        """Абстрактный метод, реализующий логику работы команды в наследнике"""
        pass

    def __eq__(self, other):
        """
        Переопределенный метод сравнения двух экземпляров команд

        :param other: команда для сравнения
        :return: `True`, если тип и значения полей совпадают; иначе `False`
        """
        if type(self).__name__ != type(other).__name__:
            return False

        return self.args == other.args and self.input_stream == other.input_stream and self.output_stream == other.output_stream

    def __str__(self):
        """
        Переопределенный метод отображения состояния объекта в строку

        :return: строковое представление объекта
        """
        return f"{type(self).__name__}{self.__dict__}"


class CatCommand(Command):
    """
    Команда `cat [FILE]` — вывести на экран содержимое файла
    """

    def execute(self):
        pass


class EchoCommand(Command):
    """
    Команда `echo` — вывести на экран свой аргумент (или аргументы)
    """

    def execute(self):
        if len(self.args) == 0:
            if self.input_stream is None:
                output = sys.stdin.read()
            else:
                output = self.input_stream.read()
        else:
            output = " ".join(self.args)

        output = f"{output}\n"
        if self.output_stream is None:
            sys.stdout.write(output)
        else:
            self.output_stream.write(output)
            self.output_stream.flush()


class WcCommand(Command):
    """
    Команда `wc [FILE]` — вывести количество строк, слов и байт в файле
    """

    def execute(self):
        pass


class PwdCommand(Command):
    """
    Команда `pwd` — распечатать текущую директорию
    """

    def execute(self):
        pass


class ExitCommand(Command):
    """
    Команда `exit` — выйти из интерпретатора
    """

    def execute(self):
        pass


class AssignCommand(Command):
    """
    Команда `VAR=VAL` - сохраняет в переменные окружения указанную переменную с указанным значение
    """

    def execute(self):
        pass


class UnknownCommand(Command):
    """
    Любая другая команда, которую мы не смогли определить. Передает выполнение неизвестной команды ядру ОС
    """

    def execute(self):
        pass
