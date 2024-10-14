from typing import List

from cli_interpretator.commands.command import Command


class UserInputParser:
    """
    Модуль отвечает за преобразование входной строки в последовательность команд для последующего их исполнения
    """

    def __init__(self, cli_context):
        self.context = cli_context

    def parse(self, input_string: str) -> List[Command]:
        """
        Преобразует пользовательский ввод в последовательность экземпляров `Command`
        :param input_string: строка, введенная пользователем
        :return: список команд для выполнения
        """
        commands = []
        pipes = input_string.split('|')
        for pipe_command_string in pipes:
            pipe_command = self.__parse_command(pipe_command_string)
            commands.append(pipe_command)

        return commands

    def __parse_command(self, command_string: str) -> Command:
        pass
