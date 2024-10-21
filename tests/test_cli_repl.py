import os

import pytest

from cli_interpreter.cli_repl import REPL


@pytest.fixture
def repl():
    """Создание экземпляра REPL для тестов"""
    return REPL()


def mock_input(inputs):
    """Функция для эмуляции input() с итератором"""
    return lambda _: next(inputs, "")


def test_echo_exit(monkeypatch, repl, capsys):
    """Тест команды `echo 1; exit`"""
    inputs = iter(["echo 1", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "1\n" in captured.out


def test_cat_gitignore(monkeypatch, repl, capsys, tmp_path):
    """Тест команды `cat .gitignore`"""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.pyc\n*.log\n")

    inputs = iter([f"cat {gitignore}", "exit"])

    monkeypatch.setattr("builtins.input", mock_input(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "*.pyc\n*.log\n" in captured.out


def test_wc_gitignore(monkeypatch, repl, capsys, tmp_path):
    """Тест команды `wc .gitignore`"""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.pyc\n*.log\n")

    inputs = iter([f"wc {gitignore}", "exit"])

    monkeypatch.setattr("builtins.input", mock_input(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "2" in captured.out


def test_pwd(monkeypatch, repl, capsys, tmp_path):
    """Тест команды `pwd`"""
    inputs = iter(["pwd", "exit"])

    monkeypatch.setattr("builtins.input", mock_input(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert os.getcwd() in captured.out


def test_unknown_command(monkeypatch, repl, capsys):
    """Тест команды `ls -la`"""
    command = "ls -la"
    inputs = iter([command, "exit"])

    monkeypatch.setattr("builtins.input", mock_input(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert captured.out == os.popen(command).read()


def test_environment_variables(monkeypatch, repl, capsys):
    """Тест работы с переменными окружения"""
    inputs = iter(
        [
            "A=123 B=45",
            "echo $A$B",
            "exit",
        ]
    )

    monkeypatch.setattr("builtins.input", mock_input(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "12345\n" in captured.out


def test_pipe_echo_wc(monkeypatch, repl, capsys):
    """Тест пайпа из двух команд"""
    inputs = iter(["echo 123 | wc", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "1 1 4\n" in captured.out


@pytest.mark.skip()
def test_pipe_cat_grep_wc(monkeypatch, repl, capsys):
    """Тест пайпа из трех команд"""
    inputs = iter(["cat README.md | grep -w 'Command' | wc", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()  # TODO: поправить

    captured = capsys.readouterr()
    assert "1 1 4\n" in captured.out


@pytest.mark.skip()
def test_exit_first(monkeypatch, repl, capsys):
    """Тест пайпа из двух команд"""
    inputs = iter(["exit | echo 123 | wc", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    pass  # TODO: подумать, что мы хотим увидеть в результате
