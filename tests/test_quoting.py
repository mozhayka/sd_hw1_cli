import pytest

from cli_interpreter.cli_repl import REPL


@pytest.fixture
def repl():
    """Создание экземпляра REPL для тестов"""
    return REPL()


def test_quoting_2(monkeypatch, repl, capsys):
    """Квотирование двойными кавычками"""
    inputs = iter(["x=1", "echo \"123$x\"", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "1231\n" in captured.out


def test_quoting_1(monkeypatch, repl, capsys):
    """Квотирование одинарными кавычками"""
    inputs = iter(["x=1", "echo \'123$x\'", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "123$x\n" in captured.out


def test_quoting_21(monkeypatch, repl, capsys):
    """Квотирование двойными и одинарными кавычками"""
    inputs = iter(["x=1", "echo \"\'$x\'\"", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "1 \n" in captured.out


def test_quoting_12(monkeypatch, repl, capsys):
    """Квотирование одинарными и двойными кавычками"""
    inputs = iter(["x=1", "echo \'\"$x\"\'", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "$x\n" in captured.out


def test_real_quotes_echo(monkeypatch, repl, capsys):
    """echo в двойных кавычках"""
    inputs = iter(["\"echo\" 123", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "" in captured.out


def test_real_quotes_README(monkeypatch, repl, capsys):
    """Название файла в кавычках"""
    inputs = iter(["cat \"README.md\"", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "test" in captured.out


def test_real_quotes_spaces(monkeypatch, repl, capsys):
    """Запуск файла с пробелами в названии"""
    inputs = iter(["./\"file with spaces.sh\"", "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "123" in captured.out
