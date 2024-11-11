import sys

from cli_interpreter.commands.command import Command


class CatCommand(Command):
    """
    Команда `cat [FILE]` — вывести на экран содержимое файла
    """

    MISSING_INPUT: int = 2

    def execute(self) -> int:
        has_args = len(self.args) > 0
        if not has_args and self.input_stream is None:
            sys.stderr.write("cat: Missing file argument\n")
            return CatCommand.ILLEGAL_ARGUMENT

        try:
            if has_args:
                with open(self.args[0], "r") as file:
                    content = file.read()
            else:
                content = self.input_stream

            self._write_output(content)
            return CatCommand.OK
        except FileNotFoundError:
            sys.stderr.write(f"cat: {self.args[0]}: No such file or directory\n")
            return CatCommand.MISSING_INPUT
        except Exception as e:
            sys.stderr.write(f"cat: Error reading {file}: {e}\n")
            return CatCommand.DEFAULT_ERROR
