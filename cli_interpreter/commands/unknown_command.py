import subprocess
import sys

from cli_interpreter.commands.command import Command


class UnknownCommand(Command):
    """
    Любая другая команда, которую мы не смогли определить. Передает выполнение команды ядру ОС
    """

    def execute(self):
        try:
            arguments = [
                # считаем кавычки лишними среди аргументов, если мы передаем их на откуп терминалу
                arg.replace('"', "").replace("'", "")
                for arg in self.args
            ]
            proc_in = (
                self.input_stream.read().encode("utf-8") if self.input_stream else None
            )
            proc = subprocess.run(arguments, input=proc_in, capture_output=True)
            self._write_output(proc.stdout.decode("utf-8"))
            return proc.returncode
        except Exception as e:
            sys.stderr.write(f"{str(e)}\n")
            return UnknownCommand.DEFAULT_ERROR
