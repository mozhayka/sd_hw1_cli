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
        """TODO: реализовать, покрыть тестами, внести правки в схему классов"""
        pass
