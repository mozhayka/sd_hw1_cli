import os
import sys

from cli_interpreter.commands.command import Command


class WcCommand(Command):
    """
    Команда `wc [FILE]` — вывести количество строк, слов и байт в файле
    """

    MISSING_INPUT: int = 2

    def execute(self) -> int:
        has_args = len(self.args) > 0
        if not has_args and self.input_stream is None:
            sys.stderr.write("wc: Missing file argument\n")
            return WcCommand.ILLEGAL_ARGUMENT

        try:
            if has_args:
                absolute_path = self.context.get_working_dir_absolute_path_with_file(self.args[0])
                with open(absolute_path, "r") as file:
                    content = file.read()
            else:
                content = self.input_stream.read()

            num_lines = content.count("\n")
            num_words = len(content.split())
            num_bytes = len(content.encode("utf-8"))

            result = f"{num_lines} {num_words} {num_bytes}"
            self._write_output(result)
            return WcCommand.OK
        except FileNotFoundError:
            sys.stderr.write(f"wc: {self.args[0]}: No such file or directory\n")
            return WcCommand.MISSING_INPUT
        except Exception as e:
            sys.stderr.write(f"wc: Error reading {file}: {e}\n")
            return WcCommand.DEFAULT_ERROR
