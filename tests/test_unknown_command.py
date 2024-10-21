from unittest.mock import patch, MagicMock

from cli_interpreter.commands.unknown_command import UnknownCommand


def test_unknown_command():
    """Тест команды UnknownCommand"""
    with patch("subprocess.run") as mock_subprocess_run:
        mock_proc = MagicMock(stdout=b"foo")
        mock_subprocess_run.return_value = mock_proc

        args = ["ls", "-la"]
        cmd = UnknownCommand(args=args)
        cmd.execute()

        # Проверяем, что os.system был вызван с верным аргументом
        mock_subprocess_run.assert_called_once_with(args, capture_output=True)
