import os
import sys
from abc import ABC, abstractmethod
from typing import TextIO


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
        if args is None:
            args = []
        self.args = args
        self.input_stream = input_stream
        self.output_stream = output_stream

    @abstractmethod
    def execute(self):
        pass

    def __eq__(self, other):
        if type(self).__name__ != type(other).__name__:
            return False
        return (
            self.args == other.args
            and self.input_stream == other.input_stream
            and self.output_stream == other.output_stream
        )

    def __str__(self):
        return f"{type(self).__name__}{self.__dict__}"


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
                    if self.output_stream:
                        self.output_stream.write(content)
                        self.output_stream.flush()
                    else:
                        sys.stdout.write(content)
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
        if len(self.args) > 0:
            filename = self.args[0]
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    num_lines = content.count("\n")
                    num_words = len(content.split())
                    num_bytes = len(content.encode("utf-8"))

                    result = f"{num_lines} {num_words} {num_bytes} {filename}\n"
                    if self.output_stream:
                        self.output_stream.write(result)
                        self.output_stream.flush()
                    else:
                        sys.stdout.write(result)
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
        if self.output_stream:
            self.output_stream.write(current_dir)
            self.output_stream.flush()
        else:
            sys.stdout.write(current_dir)


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

    def execute(self):
        if len(self.args) > 0:
            assignment = self.args[0].split("=", 1)
            if len(assignment) == 2:
                os.environ[assignment[0]] = assignment[1]
            else:
                sys.stderr.write("Invalid variable assignment\n")
        else:
            sys.stderr.write("No arguments for variable assignment\n")


class UnknownCommand(Command):
    """
    Любая другая команда, которую мы не смогли определить. Передает выполнение команды ядру ОС
    """

    def execute(self):
        command = " ".join(self.args)
        os.system(command)


def parse_command(input_string: str):
    """
    Разбирает строку команды и возвращает соответствующий объект команды
    """
    tokens = input_string.strip().split()

    if len(tokens) == 0:
        return None

    if tokens[0] == "cat":
        return CatCommand(args=tokens[1:])
    elif tokens[0] == "echo":
        return EchoCommand(args=tokens[1:])
    elif tokens[0] == "wc":
        return WcCommand(args=tokens[1:])
    elif tokens[0] == "pwd":
        return PwdCommand(args=tokens[1:])
    elif tokens[0] == "exit":
        return ExitCommand(args=tokens[1:])
    elif "=" in tokens[0]:
        return AssignCommand(args=[tokens[0]])
    else:
        return UnknownCommand(args=tokens)


def main():
    while True:
        try:
            input_command = input("shell> ")
            command = parse_command(input_command)
            if command:
                command.execute()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt. Type 'exit' to quit.")
        except EOFError:
            print("\nEOFError. Exiting.")
            break


if __name__ == "__main__":
    main()
