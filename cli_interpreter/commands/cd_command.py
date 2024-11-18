import os
from pathlib import Path
import sys

from cli_interpreter.commands.command import Command
from cli_interpreter.context import CliContext


class CdCommand(Command):
    """
    Команда `cd [FILE]` — изменить текущую рабочую директорию. Без аргументов меняет директорию на корневую.
    """

    def __init__(self, args: list[str], context: CliContext):
        super().__init__(args, context=context)

    def execute(self) -> int:
        HOME_DIR = '~'
        args_len = len(self.args)
        if args_len > 1:
            sys.stderr.write("cd: Too many arguments. Provide 0 or 1 arguments.\n")
            return CdCommand.ILLEGAL_ARGUMENT

        try:
            if args_len:
                new_dir = self.args[0]

                if new_dir.split('/')[0] == HOME_DIR:
                    absolute_path = Path(new_dir).expanduser()
                else:
                    absolute_path = Path(os.path.join(self.context.get_working_dir(), new_dir)).expanduser().resolve()

                if not os.path.exists(absolute_path):
                    raise Exception(f"no such file or directory: {new_dir}")
                
                if os.path.isdir(absolute_path):
                    self.context.set_working_dir(str(absolute_path))
                else:
                    raise Exception(f"not a directory: {new_dir}")
            else:
                self.context.set_working_dir(str(Path(HOME_DIR).expanduser()))

            return CdCommand.OK
        except Exception as e:
            sys.stderr.write(f"cd: {e}\n")
            return CdCommand.MISSING_INPUT
            