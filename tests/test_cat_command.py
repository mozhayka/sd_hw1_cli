import io
from unittest.mock import patch

from cli_interpreter.commands.cat_command import CatCommand


def test_cat_command_with_existing_file(tmp_path):
    """Тест команды CatCommand для файла, который существует"""
    test_content = "Hello, this is a test."
    file_path = tmp_path / "test.txt"
    file_path.write_text(test_content)

    output_stream = io.StringIO()

    cmd = CatCommand(args=[str(file_path)], output_stream=output_stream)
    assert CatCommand.OK == cmd.execute()

    output = output_stream.getvalue()
    assert output == test_content


def test_cat_command_with_missing_file():
    """Тест команды CatCommand для несуществующего файла"""
    output_stream = io.StringIO()

    cmd = CatCommand(args=["non_existing_file.txt"], output_stream=output_stream)

    # Перехватываем вывод в stderr с помощью patch
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        assert CatCommand.MISSING_INPUT == cmd.execute()
        error_output = mock_stderr.getvalue().strip()

    # Проверяем, что вывод в stderr содержит сообщение об ошибке
    assert "non_existing_file.txt" in error_output
