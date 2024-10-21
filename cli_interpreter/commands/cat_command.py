import sys

from cli_interpreter.commands.command import Command


class CatCommand(Command):
    """
    Команда `cat [FILE]` — вывести на экран содержимое файла
    """

    def execute(self):
        if len(self.args) > 0:
            filename = self.args[0]
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    self._write_output(content)
            except FileNotFoundError:
                sys.stderr.write(f"cat: {filename}: No such file or directory\n")
            except Exception as e:
                sys.stderr.write(f"cat: Error reading {filename}: {e}\n")
        else:
            sys.stderr.write("cat: Missing file argument\n")
