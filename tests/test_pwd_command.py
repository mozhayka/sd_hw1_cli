import io
import os

from cli_interpreter.commands.pwd_command import PwdCommand
from cli_interpreter.context import CliContext


def test_pwd_command():
    """Тест команды PwdCommand"""
    current_working_dir = os.getcwd()
    output_stream = io.StringIO()

    cmd = PwdCommand(output_stream=output_stream, context=CliContext())
    assert PwdCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip()
    assert output == current_working_dir
