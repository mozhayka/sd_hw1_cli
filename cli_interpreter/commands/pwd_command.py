import os
from typing import TextIO

from cli_interpreter.commands.command import Command
from cli_interpreter.context import CliContext


class PwdCommand(Command):
    """
    Команда `pwd` — распечатать текущую директорию
    """

    def __init__(self, args: list[str] = None, input_stream: TextIO = None, output_stream: TextIO = None, context: CliContext = None):
        super().__init__(args=args, input_stream=input_stream, output_stream=output_stream, context=context)

    def execute(self) -> int:
        working_dir = self.context.get_working_dir()
        self._write_output(working_dir)
        return PwdCommand.OK
