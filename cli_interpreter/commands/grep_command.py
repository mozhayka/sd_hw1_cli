import argparse
import os
import re
import sys

from cli_interpreter.commands.command import Command


class GrepCommand(Command):
    """
    Команда `grep`.

    Требуется поддержка:
        - регулярных выражений в запросе;
        - ключа -w — поиск только слова целиком;
        - ключа -i — регистронезависимый (case-insensitive) поиск;
        - ключа -A — следующее за -A число говорит, сколько строк после совпадения надо распечатать.

    Примеры:
        - `grep "Минимальный$" README.md`
        - `grep -w "Минимал" README.md > grep -A 1 "II" README.md`
    """

    def __init__(self, args: list[str], context):
        """
        Конструктор инициализирует утилиту для разбора аргументов команды `grep`
        @:param args - аргументы, полученные из пользовательского ввода
        """
        super().__init__(args=args, context=context)

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("word", type=str, help="искомое слово")
        parser.add_argument(
            "file", type=str, nargs="?", default=None, help="файл, в котором ищем"
        )
        parser.add_argument(
            "-w", action="store_true", help="поиск только слова целиком"
        )
        parser.add_argument(
            "-i",
            action="store_true",
            help="регистронезависимый (case-insensitive) поиск",
        )
        parser.add_argument(
            "-A",
            type=int,
            default=0,
            help="сколько строк после совпадения надо распечатать",
        )
        self.arg_parser = parser

    def execute(self) -> int:
        word, filename, w_flag, i_flag, a_flag = self.__parse_arguments()
        pattern, regex_flags = self.__resolve_regexp_parameters(word, i_flag, w_flag)

        try:
            if self.input_stream is None:
                absolute_path = self.context.get_working_dir_absolute_path_with_file(filename)
                with open(absolute_path, "r") as file:
                    content = file.readlines()
            else:
                content = self.input_stream.read().split("\n")

            # Построчно парсим
            matches = []
            for i, line in enumerate(content):
                if re.search(pattern, line, regex_flags):
                    matches.append(line.strip())
                    if a_flag > 0:
                        matches.extend(content[i + 1: i + 1 + a_flag])

            self._write_output("\n".join(matches))
            return Command.OK
        except FileNotFoundError:
            sys.stderr.write(f"grep: {filename}: No such file or directory\n")
            return Command.ILLEGAL_ARGUMENT

    def __parse_arguments(self) -> (str, str, bool, bool, int):
        """Парсим аргументы"""

        try:
            command_args = self.args
            args = self.arg_parser.parse_args(command_args)
            return args.word, args.file, args.w, args.i, args.A
        except SystemExit as e:
            raise RuntimeError("Произошла ошибка при разборе аргументов")

    @staticmethod
    def __resolve_regexp_parameters(
            word: str, i_flag: bool, w_flag: bool
    ) -> (str, int):
        """Настраиваем параметры поиска"""
        regex_flags = 0
        if i_flag:
            regex_flags |= re.IGNORECASE

        if w_flag:
            pattern = r"\b" + re.escape(word) + r"\b"  # ищем только целое слово
        else:
            pattern = word

        return pattern, regex_flags
