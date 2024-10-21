from cli_interpreter.commands.assign_command import AssignCommand
from cli_interpreter.context import CliContext


def test_assign_command():
    expected_env = "A"
    expected_value = "1"

    context = CliContext()
    assert context.get(expected_env) == ""

    command = AssignCommand(args=[expected_env, expected_value], context=context)
    assert AssignCommand.OK == command.execute()

    assert context.get(expected_env) == expected_value
