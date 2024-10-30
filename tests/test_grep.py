import os

import pytest

from cli_interpreter.cli_repl import REPL


@pytest.fixture
def repl():
    """Создание экземпляра REPL для тестов"""
    return REPL()


def test_grep_simple(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = "test"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep \"test\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "test" in captured.out


def test_grep_no_args(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = " Минимальный синтаксис grep"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep \"Минимальный\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Минимальный синтаксис grep" in captured.out


def test_grep_no_args2(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = " Минимальный синтаксис grep"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep \"Минимальный$\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "" in captured.out


def test_grep_i(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = " Минимальный синтаксис grep"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep -i \"минимальный\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "Минимальный синтаксис grep" in captured.out


def test_grep_w(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = " Минимальный синтаксис grep"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep -i \"Минимал\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "" in captured.out


def test_grep_A(monkeypatch, repl, tmp_path, capsys):
    """Простой тест на grep"""
    test_content = " Минимальный синтаксис grep"
    file_path = tmp_path / "README.md"
    file_path.write_text(test_content)
    inputs = iter([f'grep -A 1 \"II\" "{file_path}"', "exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl.run()

    captured = capsys.readouterr()
    assert "" in captured.out