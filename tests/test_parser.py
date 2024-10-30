import pytest

from cli_interpreter.commands.assign_command import AssignCommand
from cli_interpreter.commands.cat_command import CatCommand
from cli_interpreter.commands.echo_command import EchoCommand
from cli_interpreter.commands.exit_command import ExitCommand
from cli_interpreter.commands.pwd_command import PwdCommand
from cli_interpreter.commands.unknown_command import UnknownCommand
from cli_interpreter.commands.wc_command import WcCommand
from cli_interpreter.context import CliContext
from cli_interpreter.parser import UserInputParser
from cli_interpreter.commands.grep_command import GrepCommand

context: CliContext
parser: UserInputParser


@pytest.fixture(autouse=True)
def set_up():
    global context, parser
    context = CliContext()
    parser = UserInputParser(cli_context=context)
    yield


def test_cat_command():
    commands = parser.parse("cat foo")
    assert len(commands) == 1
    assert commands[0] == CatCommand(["foo"])


def test_echo_command():
    commands = parser.parse("echo foo bar")
    assert len(commands) == 1
    assert commands[0] == EchoCommand(["foo", "bar"])


def test_wc_command():
    commands = parser.parse("wc foo")
    assert len(commands) == 1
    assert commands[0] == WcCommand(["foo"])


def test_pwd_command():
    commands = parser.parse("pwd")
    assert len(commands) == 1
    assert commands[0] == PwdCommand()


def test_exit_command():
    commands = parser.parse("exit")
    assert len(commands) == 1
    assert commands[0] == ExitCommand()


def test_unknown_command():
    commands = parser.parse("ls -l")
    assert len(commands) == 1
    assert commands[0] == UnknownCommand(["ls", "-l"])


def test_assignment():
    commands = parser.parse("A=1 B=\"foo bar\"")
    assert len(commands) == 1
    assert commands[0] == AssignCommand(["A", "1", "B", "foo bar"], context)


def test_ignore_assignment():
    commands = parser.parse("A=1 B=2 echo foo")
    assert len(commands) == 1
    assert commands[0] == EchoCommand(["foo"])


def test_substitution():
    context.set("A", "foo")
    commands = parser.parse("echo $A")
    assert len(commands) == 1
    assert commands[0] == EchoCommand(["foo"])


def test_substitution_weak_quoting():
    context.set("A", "foo")
    commands = parser.parse('echo "$A"')
    assert len(commands) == 1
    assert commands[0] == EchoCommand(["foo"])


def test_substitution_full_quoting():
    context.set("A", "foo")
    commands = parser.parse("echo '$A'")
    assert len(commands) == 1
    assert commands[0] == EchoCommand(["$A"])


def test_substitution_before_command_resolution():
    context.set("A", "p")
    context.set("B", "wd")
    commands = parser.parse("$A$B")
    assert len(commands) == 1
    assert commands[0] == PwdCommand()


def test_pipe():
    commands = parser.parse("cat foo.txt | wc")
    assert len(commands) == 2
    assert commands[0] == CatCommand(["foo.txt"])
    assert commands[1] == WcCommand()

def test_grep():
    commands = parser.parse("grep \"test\" Readme.md")
    assert len(commands) == 1
    assert commands[0] == GrepCommand(["test",  "Readme.md", False, False, 0])

def test_grep_with_args():
    commands = parser.parse("grep -i \"test\" -A 10 Readme.md")
    assert len(commands) == 1
    assert commands[0] == GrepCommand(["test",  "Readme.md", False, True, 10])