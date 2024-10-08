import sys

from cli_interpretator.commands.command import Command


class EchoCommand(Command):
    """
    Команда `echo` — вывести на экран свой аргумент (или аргументы)
    """

    def execute(self):
        if self.args is None:
            if self.input_stream is None:
                output = sys.stdin.read()
            else:
                output = self.input_stream.read()
        else:
            output = " ".join(self.args)

        output = f"{output}\n"
        if self.output_stream is None:
            sys.stdout.write(output)
        else:
            self.output_stream.write(output)
            self.output_stream.flush()
