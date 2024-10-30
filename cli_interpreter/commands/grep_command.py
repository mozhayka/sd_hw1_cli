import argparse
import shlex
import sys
import re

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

    def execute(self) -> int:
        word = self.args[0]
        filename = self.args[1]
        w = self.args[2]
        i = self.args[3]
        A = int(self.args[4])

        """Настраиваем параметры поиска"""
        regex_flags = 0
        if i:
            regex_flags |= re.IGNORECASE

        if w:
            pattern = r'\b' + re.escape(word) + r'\b'  # ищем только целое слово
        else:
            pattern = word

        try:
            with open(filename, "r") as file:
                content = file.readlines()

                """Построчно парсим"""
                matches = []
                for i, line in enumerate(content):
                    if re.search(pattern, line, regex_flags):
                        matches.append(line.strip())
                        if A > 0:
                            matches.extend(content[i + 1:i + 1 + A])

                for match in matches:
                    self._write_output(match)
                return Command.OK
        except FileNotFoundError:
            sys.stderr.write(f"grep: {filename}: No such file or directory\n")
            return Command.ILLEGAL_ARGUMENT
