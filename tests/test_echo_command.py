import io

from cli_interpreter.commands.echo_command import EchoCommand


def test_echo_command_with_arguments():
    """Тест команды EchoCommand с аргументами"""
    args = ["Hello", "World"]
    output_stream = io.StringIO()

    cmd = EchoCommand(args=args, output_stream=output_stream)
    assert EchoCommand.OK == cmd.execute()

    output = output_stream.getvalue()
    assert output == "Hello World\n"


def test_echo_command_with_input_stream():
    """Тест команды EchoCommand с input stream"""
    expected = "Input Stream"
    input_stream = io.StringIO(expected)
    output_stream = io.StringIO()

    cmd = EchoCommand(input_stream=input_stream, output_stream=output_stream)
    assert EchoCommand.OK == cmd.execute()

    output = output_stream.getvalue()
    assert output == f"{expected}\n"
