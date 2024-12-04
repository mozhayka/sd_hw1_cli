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

                # Дополнительно обрабатываем случай знака '~', так как он не разрешается автоматически
                # Без обработки:
                # pwd: /Documents/dir1
                # cd ~: /Documents/dir1/~, а надо просто ~/
                if new_dir.split('/')[0] == HOME_DIR:
                    absolute_path = Path(new_dir).expanduser()
                else:
                    absolute_path = Path(self.context.get_working_dir_absolute_path_with_file(new_dir)).expanduser().resolve()

                if not os.path.exists(absolute_path):
                    raise FileNotFoundError(f"no such file or directory: {new_dir}")
                
                if not os.path.isdir(absolute_path):
                    raise FileNotFoundError(f"not a directory: {new_dir}")

                self.context.set_working_dir(str(absolute_path))
                    
            else:
                self.context.set_working_dir(str(Path(HOME_DIR).expanduser()))

            return CdCommand.OK
        except FileNotFoundError as e:
            sys.stderr.write(f"cd: {e}\n")
            return CdCommand.MISSING_INPUT
        except Exception as e:
            return CdCommand.DEFAULT_ERROR
            