import os

from cli_interpreter.commands.command import Command


class PwdCommand(Command):
    """
    Команда `pwd` — распечатать текущую директорию
    """

    def execute(self) -> int:
        current_dir = os.getcwd() + "\n"
        self._write_output(current_dir)
        return PwdCommand.OK
