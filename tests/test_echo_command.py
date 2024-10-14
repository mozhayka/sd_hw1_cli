import io

from cli_interpreter.commands import EchoCommand


def test_execute_with_arguments(monkeypatch):
    output_stream = io.StringIO()
    monkeypatch.setattr("sys.stdout", output_stream)

    cmd = EchoCommand(["Hello,", "world!"])
    cmd.execute()

    output = output_stream.getvalue()
    assert output == "Hello, world!\n"


def test_execute_with_input_stream(monkeypatch):
    expected = "Input Stream"
    input_stream = io.StringIO(expected)
    output_stream = io.StringIO()
    monkeypatch.setattr('sys.stdout', output_stream)

    cmd = EchoCommand(input_stream=input_stream)
    cmd.execute()

    output = output_stream.getvalue()
    assert output == f"{expected}\n"


def test_execute_with_input_and_output_streams():
    expected = "Input Stream"
    input_stream = io.StringIO(expected)
    output_stream = io.StringIO()

    cmd = EchoCommand(input_stream=input_stream, output_stream=output_stream)
    cmd.execute()

    output = output_stream.getvalue()
    assert output == f"{expected}\n"
