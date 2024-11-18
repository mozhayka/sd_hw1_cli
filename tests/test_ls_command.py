import io
import os
import time
from unittest.mock import patch

from cli_interpreter.commands.ls_command import LsCommand
from cli_interpreter.context import CliContext


def test_ls_command_default():
    """Тест команды LsCommand без аргументов для существующей директории"""
    files = ('file1.txt', 'file2.txt', '.hidden_file', 'dir1')

    output_stream = io.StringIO()

    cmd = LsCommand(args=[], output_stream=output_stream, input_stream=None, context=CliContext())

    with patch("os.listdir", return_value=files):
        assert LsCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip().split('\n')
    expected = sorted(["file1.txt", "file2.txt", "dir1"])
    assert output == expected


def test_ls_command_non_existing_directory():
    """Тест команды LsCommand для несуществующей директории"""
    output_stream = io.StringIO()

    cmd = LsCommand(args=["non_existing_dir"], output_stream=output_stream, input_stream=None, context=CliContext())

    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        assert LsCommand.ILLEGAL_ARGUMENT == cmd.execute()
        error_output = mock_stderr.getvalue().strip()

    assert "ls: cannot access 'non_existing_dir': No such file or directory" in error_output


def test_ls_command_with_a_option(tmp_path):
    """Тест команды LsCommand с опцией -a для отображения скрытых файлов"""
    (tmp_path / "file1.txt").write_text("Content of file1")
    (tmp_path / ".hidden_file").write_text("Hidden content")
    (tmp_path / "dir1").mkdir()

    output_stream = io.StringIO()

    cmd = LsCommand(args=["-a", str(tmp_path)], output_stream=output_stream, input_stream=None, context=CliContext())

    assert LsCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip().split('\n')
    expected = sorted([".", "..", "file1.txt", ".hidden_file", "dir1"])
    assert output == expected


def test_ls_command_with_l_option(tmp_path):
    """Тест команды LsCommand с опцией -l для подробного вывода с выравниванием столбцов и 'total'"""

    file1 = tmp_path / "file1.txt"
    file1.write_text("Content of file1")
    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    stats_file1 = os.lstat(file1)
    stats_dir1 = os.lstat(dir1)

    expected_total = getattr(stats_file1, 'st_blocks', 0) + getattr(stats_dir1, 'st_blocks', 0)

    output_stream = io.StringIO()

    cmd = LsCommand(args=["-l", str(tmp_path)], output_stream=output_stream, input_stream=None, context=CliContext())

    assert LsCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip().split('\n')
    assert len(output) == 3

    assert output[0].startswith("total ")
    actual_total = int(output[0].split()[1])
    assert actual_total == expected_total

    for line, entry in zip(output[1:], ["dir1", "file1.txt"]):
        parts = line.split()
        assert len(parts) >= 7
        assert parts[-1] == entry


def test_ls_command_with_t_option(tmp_path):
    """Тест команды LsCommand с опцией -t для сортировки по дате создания"""

    file1 = tmp_path / "file1.txt"
    file1.write_text("Content of file1")
    time.sleep(1)
    file2 = tmp_path / "file2.txt"
    file2.write_text("Content of file2")

    output_stream = io.StringIO()

    cmd = LsCommand(args=["-t", str(tmp_path)], output_stream=output_stream, input_stream=None, context=CliContext())

    assert LsCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip().split('\n')

    expected = ["file2.txt", "file1.txt"]
    assert output == expected


def test_ls_command_with_all_options(tmp_path):
    """Тест команды LsCommand с опциями -a, -l и -t, включая строку 'total'"""

    file1 = tmp_path / "file1.txt"
    file1.write_text("Content of file1")
    time.sleep(0.5)
    file2 = tmp_path / "file2.txt"
    file2.write_text("Content of file2")
    time.sleep(0.5)
    hidden_file = tmp_path / ".hidden_file"
    hidden_file.write_text("Hidden content")
    time.sleep(0.5)
    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    time.sleep(0.5)
    dir2 = tmp_path / "dir2"
    dir2.mkdir()

    stats_file1 = os.lstat(file1)
    stats_file2 = os.lstat(file2)
    stats_hidden = os.lstat(hidden_file)
    stats_dir1 = os.lstat(dir1)
    stats_dir2 = os.lstat(dir2)

    expected_total = (
            getattr(stats_file1, 'st_blocks', 0) +
            getattr(stats_file2, 'st_blocks', 0) +
            getattr(stats_hidden, 'st_blocks', 0) +
            getattr(stats_dir1, 'st_blocks', 0) +
            getattr(stats_dir2, 'st_blocks', 0)
    )

    output_stream = io.StringIO()

    cmd = LsCommand(args=["-a", "-l", "-t", str(tmp_path)], output_stream=output_stream, input_stream=None, context=CliContext())

    assert LsCommand.OK == cmd.execute()

    output = output_stream.getvalue().strip().split('\n')

    assert len(output) == 8

    assert output[0].startswith("total ")
    actual_total = int(output[0].split()[1])
    assert actual_total == expected_total

    expected_order = ["dir2", ".", "dir1", ".hidden_file", "file2.txt", "file1.txt", ".."]
    actual_order = [line.split()[-1] for line in output[1:]]
    assert actual_order == expected_order
