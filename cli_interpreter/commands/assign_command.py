import sys

from cli_interpreter.commands.command import Command
from cli_interpreter.context import CliContext


class AssignCommand(Command):
    """
    Команда `VAR=VAL [VAR1=VAL1 ...]` - сохраняет в переменные окружения указанную переменную с указанным значением
    """

    def __init__(self, args: list[str], context: CliContext):
        super().__init__(args)
        self.context = context

    def execute(self):
        assert len(self.args) % 2 == 0  # Количество аргументов должно быть четным

        if len(self.args) == 0:
            sys.stderr.write("No arguments for variable assignment\n")
            return

        for i in range(0, len(self.args), 2):
            env_variable = self.args[i]
            env_value = self.args[i + 1]
            self.context.set(env_variable, env_value)
