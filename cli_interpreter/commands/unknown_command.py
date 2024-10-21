import subprocess

from cli_interpreter.commands.command import Command


class UnknownCommand(Command):
    """
    Любая другая команда, которую мы не смогли определить. Передает выполнение команды ядру ОС
    """

    def execute(self):
        output = subprocess.run(self.args, capture_output=True)
        self._write_output(output.stdout.decode("utf-8"))
