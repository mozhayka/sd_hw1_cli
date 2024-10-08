import sys
from abc import ABC, abstractmethod
from typing import List, TextIO


class Command(ABC):
    """
    Базовый класс команды, хранящий данные для выполнения команды
    """

    def __init__(self, command: str,
                 args: List[str] = None,
                 input_stream: TextIO = sys.stdin,
                 output_stream: TextIO = sys.stdout):
        """Конструктор класса команды
        :param command: тип команды
        :param args: список строк-аргументов команды
        :param input_stream: поток ввода
        :param output_stream: поток вывода
        """
        if args is None:
            args = []

        self.command = command
        self.args = args
        self.input_stream = input_stream
        self.output_stream = output_stream

    @abstractmethod
    def execute(self):
        """Абстрактный метод, реализующий логику работы команды в наследнике"""
        pass
