import io
import os
from unittest.mock import patch, MagicMock

from cli_interpreter.commands import (
    EchoCommand,
    CatCommand,
    WcCommand,
    PwdCommand,
    ExitCommand,
    UnknownCommand,
    AssignCommand,
)
from cli_interpreter.context import CliContext


def test_echo_command_with_arguments():
    """Тест команды EchoCommand с аргументами"""
    args = ["Hello", "World"]
    output_stream = io.StringIO()

    cmd = EchoCommand(args=args, output_stream=output_stream)
    cmd.execute()

    output = output_stream.getvalue()
    assert output == "Hello World\n"


def test_echo_command_with_input_stream():
    """Тест команды EchoCommand с input stream"""
    expected = "Input Stream"
    input_stream = io.StringIO(expected)
    output_stream = io.StringIO()

    cmd = EchoCommand(input_stream=input_stream, output_stream=output_stream)
    cmd.execute()

    output = output_stream.getvalue()
    assert output == f"{expected}\n"


def test_cat_command_with_existing_file(tmp_path):
    """Тест команды CatCommand для файла, который существует"""
    test_content = "Hello, this is a test."
    file_path = tmp_path / "test.txt"
    file_path.write_text(test_content)

    output_stream = io.StringIO()

    cmd = CatCommand(args=[str(file_path)], output_stream=output_stream)
    cmd.execute()

    output = output_stream.getvalue()
    assert output == test_content


def test_cat_command_with_missing_file():
    """Тест команды CatCommand для несуществующего файла"""
    output_stream = io.StringIO()

    cmd = CatCommand(args=["non_existing_file.txt"], output_stream=output_stream)

    # Перехватываем вывод в stderr с помощью patch
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        cmd.execute()
        error_output = mock_stderr.getvalue().strip()

    # Проверяем, что вывод в stderr содержит сообщение об ошибке
    assert "non_existing_file.txt" in error_output


def test_wc_command_with_existing_file(tmp_path):
    """Тест команды WcCommand для файла, который существует"""
    test_content = "Line 1\nLine 2\n"
    file_path = tmp_path / "test.txt"
    file_path.write_text(test_content)

    output_stream = io.StringIO()

    cmd = WcCommand(args=[str(file_path)], output_stream=output_stream)
    cmd.execute()

    # Ожидаем количество строк, слов и байтов
    output = output_stream.getvalue().strip()
    lines, words, bytes_count, filename = output.split()
    assert int(lines) == 2
    assert int(words) == 4
    assert int(bytes_count) == len(test_content)
    assert filename == str(file_path)


def test_wc_command_with_missing_file():
    """Тест команды WcCommand для несуществующего файла"""
    output_stream = io.StringIO()

    cmd = WcCommand(args=["non_existing_file.txt"], output_stream=output_stream)

    # Перехватываем вывод в stderr с помощью patch
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        cmd.execute()
        error_output = mock_stderr.getvalue().strip()

    # Проверяем, что вывод в stderr содержит сообщение об ошибке
    assert "non_existing_file.txt" in error_output


def test_pwd_command():
    """Тест команды PwdCommand"""
    current_working_dir = os.getcwd()
    output_stream = io.StringIO()

    cmd = PwdCommand(output_stream=output_stream)
    cmd.execute()

    output = output_stream.getvalue().strip()
    assert output == current_working_dir


def test_exit_command():
    """Тест команды ExitCommand для выхода"""
    with patch("sys.exit") as mock_exit:
        cmd = ExitCommand()
        cmd.execute()

        # Проверяем, что вызван sys.exit(0)
        mock_exit.assert_called_once_with(0)


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


def test_assign_command():
    expected_env = "A"
    expected_value = "1"

    context = CliContext()
    assert context.get(expected_env) == ""

    command = AssignCommand(args=[expected_env, expected_value], context=context)
    command.execute()

    assert context.get(expected_env) == expected_value
