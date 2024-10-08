from abc import ABC, abstractmethod
from typing import List, TextIO


class Command(ABC):
    """
    Базовый класс команды, хранящий данные для выполнения команды
    """

    def __init__(self,
                 args: List[str] = None,
                 input_stream: TextIO = None,
                 output_stream: TextIO = None):
        """Конструктор класса команды
        :param args: список строк-аргументов команды
        :param input_stream: поток ввода
        :param output_stream: поток вывода
        """
        self.args = args
        self.input_stream = input_stream
        self.output_stream = output_stream

    @abstractmethod
    def execute(self):
        """Абстрактный метод, реализующий логику работы команды в наследнике"""
        pass
