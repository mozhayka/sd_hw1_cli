import os
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import TextIO

from cli_interpreter.context import CliContext


class Command(ABC):
    """
    Базовый класс команды, хранящий данные для выполнения команды
    """

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
        if self.output_stream:
            self.output_stream.write(output)
            self.output_stream.flush()
        else:
            sys.stdout.write(output)
            sys.stdout.flush()


class CatCommand(Command):
    """
    Команда `cat [FILE]` — вывести на экран содержимое файла
    """

    def execute(self):
        if len(self.args) > 0:
            filename = self.args[0]
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    self._write_output(content)
            except FileNotFoundError:
                sys.stderr.write(f"cat: {filename}: No such file or directory\n")
            except Exception as e:
                sys.stderr.write(f"cat: Error reading {filename}: {e}\n")
        else:
            sys.stderr.write("cat: Missing file argument\n")


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
        self._write_output(output)


class WcCommand(Command):
    """
    Команда `wc [FILE]` — вывести количество строк, слов и байт в файле
    """

    def execute(self):
        if len(self.args) > 0:
            filename = self.args[0]
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    num_lines = content.count("\n")
                    num_words = len(content.split())
                    num_bytes = len(content.encode("utf-8"))

                    result = f"{num_lines} {num_words} {num_bytes} {filename}\n"
                    self._write_output(result)
            except FileNotFoundError:
                sys.stderr.write(f"wc: {filename}: No such file or directory\n")
            except Exception as e:
                sys.stderr.write(f"wc: Error reading {filename}: {e}\n")
        else:
            sys.stderr.write("wc: Missing file argument\n")


class PwdCommand(Command):
    """
    Команда `pwd` — распечатать текущую директорию
    """

    def execute(self):
        current_dir = os.getcwd() + "\n"
        self._write_output(current_dir)


class ExitCommand(Command):
    """
    Команда `exit` — выйти из интерпретатора
    """

    def execute(self):
        sys.exit(0)


class AssignCommand(Command):
    """
    Команда `VAR=VAL` - сохраняет в переменные окружения указанную переменную с указанным значением
    """

    def __init__(self, args: list[str], context: CliContext):
        super().__init__(args)
        self.context = context

    def execute(self):
        if len(self.args) > 0:
            self.context.set(self.args[0], self.args[1])
        else:
            sys.stderr.write("No arguments for variable assignment\n")


class UnknownCommand(Command):
    """
    Любая другая команда, которую мы не смогли определить. Передает выполнение команды ядру ОС
    """

    def execute(self):
        output = subprocess.run(self.args, capture_output=True)
        self._write_output(output.stdout.decode("utf-8"))
