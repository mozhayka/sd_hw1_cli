import os
from unittest.mock import patch, MagicMock

from cli_interpreter.commands.unknown_command import UnknownCommand
from cli_interpreter.context import CliContext


def test_unknown_command_success():
    """Тест успешного выполнения команды UnknownCommand"""
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = b"foo\n"
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        args = ["ls", "-la"]
        context = CliContext()
        cmd = UnknownCommand(args=args, context=context)
        cmd._write_output = MagicMock()

        assert UnknownCommand.OK == cmd.execute()

        mock_run.assert_called_once_with(args, input=None, capture_output=True, cwd=context.get_working_dir())
        cmd._write_output.assert_called_once_with("foo\n")


def test_unknown_command_with_input_stream():
    """Тест команды UnknownCommand с переданным input_stream"""
    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.stdout = b"bar\n"
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        input_stream = MagicMock()
        input_stream.read.return_value = "input text"

        args = ["grep", "pattern"]
        context = MagicMock()
        context.get_working_dir.return_value = os.getcwd()
        cmd = UnknownCommand(args=args, input_stream=input_stream, context=context)
        cmd._write_output = MagicMock()

        assert UnknownCommand.OK == cmd.execute()

        mock_run.assert_called_once_with(args, input="input text".encode("utf-8"), capture_output=True, cwd=context.get_working_dir())
        cmd._write_output.assert_called_once_with("bar\n")


def test_unknown_command_failure():
    """Тест команды UnknownCommand, которая завершается ошибкой"""
    with patch("subprocess.run") as mock_run:
        expected_return_code = 420
        mock_proc = MagicMock()
        mock_proc.stdout = b""
        mock_proc.returncode = expected_return_code
        mock_run.return_value = mock_proc

        args = ["ls", "non_existent_file"]
        context = CliContext()
        cmd = UnknownCommand(args=args, context=context)
        cmd._write_output = MagicMock()

        assert expected_return_code == cmd.execute()

        mock_run.assert_called_once_with(args, input=None, capture_output=True, cwd=context.get_working_dir())
        cmd._write_output.assert_called_once_with("")


def test_unknown_command_exception():
    """Тест команды UnknownCommand, которая вызывает исключение"""
    with patch("subprocess.run", side_effect=Exception("Test error")) as mock_run:
        args = ["ls", "-la"]
        context = CliContext()
        cmd = UnknownCommand(args=args, context=context)

        with patch("sys.stderr", new_callable=MagicMock) as mock_stderr:
            assert UnknownCommand.DEFAULT_ERROR == cmd.execute()
            mock_run.assert_called_once_with(args, input=None, capture_output=True, cwd=context.get_working_dir())
            mock_stderr.write.assert_called_once_with("Test error\n")
