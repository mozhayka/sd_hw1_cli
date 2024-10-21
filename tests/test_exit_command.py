from unittest.mock import patch

from cli_interpreter.commands.exit_command import ExitCommand


def test_exit_command():
    """Тест команды ExitCommand для выхода"""
    with patch("sys.exit") as mock_exit:
        cmd = ExitCommand()
        cmd.execute()

        # Проверяем, что вызван sys.exit(0)
        mock_exit.assert_called_once_with(0)
