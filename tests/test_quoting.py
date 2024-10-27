import os
import re

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


