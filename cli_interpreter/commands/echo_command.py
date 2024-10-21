import sys

from cli_interpreter.commands.command import Command


class EchoCommand(Command):
    """
    Команда `echo` — вывести на экран свой аргумент (или аргументы)
    """

    def execute(self):
        if len(self.args) == 0:
            if self.input_stream is None:
                output = sys.stdin.read()
            else:
                output = self.input_stream.read()
        else:
            output = " ".join(self.args)

        output = f"{output}\n"
        self._write_output(output)
