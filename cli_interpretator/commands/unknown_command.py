import sys

from cli_interpretator.commands.command import Command


class UnknownCommand(Command):
    """
    Обработчик команды, который передает её as-is в ядро ОС через os.system()
    """

    def execute(self):
        # TODO
        pass
