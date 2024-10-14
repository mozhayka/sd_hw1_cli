import re
import shlex

from cli_interpreter.commands import (
    Command,
    CatCommand,
    EchoCommand,
    WcCommand,
    PwdCommand,
    ExitCommand,
    UnknownCommand,
    AssignCommand,
)
from cli_interpreter.context import CliContext


class UserInputParser:
    """
    Модуль отвечает за преобразование входной строки в последовательность команд для последующего их исполнения
    """

    def __init__(self, cli_context: CliContext):
        self.context = cli_context

    def parse(self, input_string: str) -> list[Command]:
        """
        Преобразует пользовательский ввод в последовательность экземпляров `Command`

        :param input_string: строка, введенная пользователем
        :return: список команд для выполнения
        """
        commands: list[Command] = []
        command_strings = input_string.split(
            "|"
        )  # Если это pipeline, разобьём его на команды
        for command_string in command_strings:
            tokens = self.__tokenize_command(
                command_string
            )  # Разделим строку команды на токены
            tokens = self.__substitute_envs(
                tokens
            )  # Подставляем значения из переменных окружения
            assignment, tokens = self.__extract_assignments(
                tokens
            )  # Извлечем операции присвоения

            if (
                    assignment  # Если строка состоит из операций присвоения
                    and not tokens  # И других токенов нет
            ):
                return [assignment]  # Вернем команды присвоения переменных окружения

            command = self.__create_command(
                tokens
            )  # Иначе создадим команду на основе имеющихся токенов, игнорируя присвоения
            commands.append(command)

        return commands

    def __tokenize_command(self, command_string: str) -> list[str]:
        """
        Разделяет строку на команды с учетом кавычек

        :param command_string: строка команды
        :return: список токенов
        """
        tokens = shlex.shlex(command_string, posix=False)
        tokens.whitespace_split = True
        tokens.escapedquotes = True
        return list(iter(tokens.get_token, ""))

    def __substitute_envs(self, tokens: list[str]) -> list[str]:
        """
        Подставляет значения переменных окружения в токены.
        Если токен ограничен одинарными кавычками, подстановку не выполняет

        :param tokens: список токенов
        :return: список токенов с подставленными значениями переменных окружения
        """
        substituted_tokens = []
        for token in tokens:
            if token.startswith("'") and token.endswith("'"):
                substituted_tokens.append(
                    token
                )  # Пропускаем токены, начинающиеся в одинарных кавычках
                continue

            substituted_token = re.sub(r"\$(\w+)", self.__replace_env, token)
            substituted_tokens.append(substituted_token)

        return substituted_tokens

    def __replace_env(self, match: re.Match) -> str:
        """
        По найденному совпадению извлекает значение переменной окружения и запрашивает её значение

        :param match: найденное совпадение регулярного выражения
        :return: значение переменной окружения
        """
        variable = match.group(1)
        return self.context.get(variable)

    def __extract_assignments(
        self, tokens: list[str]
    ) -> (AssignCommand | None, list[str]):
        """
        Извлекает из токенов все впереди идущие операции присвоения

        :param tokens: список токенов команды
        :return: кортеж из команд присвоения и оставшихся токенов, если такие есть
        """
        assignments: list[str] = (
            []
        )  # список, хранящий пары аргументов для операций присвоения

        i = 0
        while i < len(tokens):
            token = tokens[i]
            assignment_params = token.split(
                "=", 1
            )  # Разделяем присвоение на переменную и значение
            if len(assignment_params) == 2:
                variable = assignment_params[0]
                if not re.fullmatch(r"\w+", variable):
                    break  # Если это не валидное имя переменной, прекратим обработку

                value = assignment_params[1]
                if not re.fullmatch(r"(\w+|\".*\"|\'.*\')", value):
                    break  # Если это не валидное значение переменной, прекратим обработку
                else:
                    value = self.__strip_single_argument_quotes(value)

                assignments.append(variable)
                assignments.append(value)
            else:
                break
            i += 1

        assignment_command = (
            AssignCommand(args=assignments, context=self.context)
            if len(assignments) > 0
            else None
        )
        return assignment_command, tokens[i:]

    def __create_command(self, tokens: list[str]) -> Command:
        """Создает команду на основе токенов

        :param tokens: список токенов команды
        :return: экземпляр команды
        """
        command_name = tokens[0]
        command_args = tokens[1:] if len(tokens) > 1 else []

        # Сначала посмотрим, является ли эта команда одной из реализуемых нами
        if command_name == "cat":
            return CatCommand(self.__strip_quotes(command_args))
        elif command_name == "echo":
            return EchoCommand(self.__strip_quotes(command_args))
        elif command_name == "wc":
            return WcCommand(self.__strip_quotes(command_args))
        elif command_name == "pwd":
            return PwdCommand()
        elif command_name == "exit":
            return ExitCommand()

        return UnknownCommand(args=tokens)  # Передадим все токены на исполнение ОС

    def __strip_quotes(self, args: list[str]):
        """
        Удаляет кавычки у аргументов, если они есть

        :param args: аргументы команды
        :return: аргументы команды без кавычек
        """
        stripped = []
        for argument in args:
            stripped.append(self.__strip_single_argument_quotes(argument))
        return stripped

    def __strip_single_argument_quotes(self, argument: str):
        """
        Удаляет кавычки у строкового аргумента, если они есть

        :param argument: строковый аргумент
        :return: строковый аргумент без кавычек
        """
        return argument.strip("'\"")
