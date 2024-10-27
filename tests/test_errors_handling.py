import pytest

from cli_interpreter.cli_repl import REPL


@pytest.fixture
def repl():
    """Создание экземпляра REPL для тестов"""
    return REPL()


def test_unknown_command(monkeypatch, repl, capsys):
    """Неправильная команда"""
    inputs = iter(["asd", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Error " in captured.out


def test_bad_quotes(monkeypatch, repl, capsys):
    """Не хватает парной кавычки"""
    inputs = iter(["echo \"", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Error " in captured.out


def test_bad_pipe(monkeypatch, repl, capsys):
    """Пустая команда в пайпе"""
    inputs = iter(["cat .gitignore |", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Error " in captured.out


def test_bad_arguments(monkeypatch, repl, capsys):
    """Не хватает аргументов"""
    inputs = iter(["cat", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Error " in captured.out
