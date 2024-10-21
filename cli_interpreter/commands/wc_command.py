import sys

from cli_interpreter.commands.command import Command


class WcCommand(Command):
    """
    Команда `wc [FILE]` — вывести количество строк, слов и байт в файле
    """

    def execute(self):
        if len(self.args) > 0:
            filename = self.args[0]
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    num_lines = content.count("\n")
                    num_words = len(content.split())
                    num_bytes = len(content.encode("utf-8"))

                    result = f"{num_lines} {num_words} {num_bytes} {filename}\n"
                    self._write_output(result)
            except FileNotFoundError:
                sys.stderr.write(f"wc: {filename}: No such file or directory\n")
            except Exception as e:
                sys.stderr.write(f"wc: Error reading {filename}: {e}\n")
        else:
            sys.stderr.write("wc: Missing file argument\n")
