import io
import os
import tempfile
from unittest.mock import patch

from cli_interpreter.commands.cd_command import CdCommand
from cli_interpreter.context import CliContext
from pathlib import Path

def test_cd_command_to_homedir():
    """Тест команды CdCommand для перехода в домашнюю директорию"""
    
    context = CliContext()
    cmd = CdCommand(args="~", context=context)
    assert CdCommand.OK == cmd.execute()

    home_dir = str(Path("~").expanduser())
    assert context.get_working_dir() == home_dir

def test_cd_command_without_args():
    """Тест команды CdCommand без аргументов для перехода в домашнюю директорию"""    
    context = CliContext()
    cmd = CdCommand(args=None, context=context)
    assert CdCommand.OK == cmd.execute()

    home_dir = str(Path("~").expanduser())
    assert context.get_working_dir() == home_dir

def test_cd_command_relative_path():
    """Тест команды CdCommand с относительным путем"""
    current_working_dir = os.getcwd()
    new_dir = os.path.dirname(current_working_dir)

    context = CliContext()
    cmd = CdCommand(args=[".."], context=context)
    assert CdCommand.OK == cmd.execute()

    assert context.get_working_dir() == new_dir
    
def test_cd_command_over_root():
    """Тест команды CdCommand в путь /.."""
    context = CliContext()
    cmd = CdCommand(args=["/.."], context=context)
    assert CdCommand.OK == cmd.execute()

    assert context.get_working_dir() == "/"

def test_cd_command_non_dir():
    """Тест команды CdCommand с файлом"""
    context = CliContext()

    with tempfile.NamedTemporaryFile(mode='w+', delete=True, dir=os.getcwd()) as temp_file:
        cmd = CdCommand(args=[temp_file.name], context=context)

        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            assert CdCommand.MISSING_INPUT == cmd.execute()
            error_output = mock_stderr.getvalue().strip()
            assert error_output == f"cd: not a directory: {temp_file.name}"

def test_cd_command_non_dir():
    """Тест команды CdCommand с несуществующей директорией"""
    context = CliContext()

    cmd = CdCommand(args=["non_existent_dir"], context=context)

    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        assert CdCommand.MISSING_INPUT == cmd.execute()
        error_output = mock_stderr.getvalue().strip()
        assert error_output == "cd: no such file or directory: non_existent_dir"
