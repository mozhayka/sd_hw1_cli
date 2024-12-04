import io
from unittest.mock import patch

from cli_interpreter.commands.wc_command import WcCommand
from cli_interpreter.context import CliContext


def test_wc_command_with_existing_file(tmp_path):
    """Тест команды WcCommand для файла, который существует"""
    test_content = "Line 1\nLine 2\n"
    file_path = tmp_path / "test.txt"
    file_path.write_text(test_content)

    output_stream = io.StringIO()

    cmd = WcCommand(args=[str(file_path)], output_stream=output_stream, context=CliContext())
    assert WcCommand.OK == cmd.execute()

    # Ожидаем количество строк, слов и байтов
    output = output_stream.getvalue().strip()
    lines, words, bytes_count = output.split()
    assert int(lines) == 2
    assert int(words) == 4
    assert int(bytes_count) == len(test_content)


def test_wc_command_with_missing_file():
    """Тест команды WcCommand для несуществующего файла"""
    output_stream = io.StringIO()

    cmd = WcCommand(args=["non_existing_file.txt"], output_stream=output_stream, context=CliContext())

    # Перехватываем вывод в stderr с помощью patch
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        assert WcCommand.MISSING_INPUT == cmd.execute()
        error_output = mock_stderr.getvalue().strip()

    # Проверяем, что вывод в stderr содержит сообщение об ошибке
    assert "non_existing_file.txt" in error_output
