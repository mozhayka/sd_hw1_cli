import sys

from cli_interpreter.commands.command import Command


class ExitCommand(Command):
    """
    Команда `exit` — выйти из интерпретатора
    """

    def execute(self):
        sys.exit(0)
