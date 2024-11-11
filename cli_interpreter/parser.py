import re

from cli_interpreter.commands.assign_command import AssignCommand
from cli_interpreter.commands.cat_command import CatCommand
from cli_interpreter.commands.command import Command
from cli_interpreter.commands.echo_command import EchoCommand
from cli_interpreter.commands.exit_command import ExitCommand
from cli_interpreter.commands.pwd_command import PwdCommand
from cli_interpreter.commands.unknown_command import UnknownCommand
from cli_interpreter.commands.wc_command import WcCommand
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
        # Если это pipeline, разобьём его на команды
        command_strings = input_string.split("|")
        for command_string in command_strings:
            # Разделим строку команды на токены
            tokens = self.__tokenize_command(command_string)
            # Подставляем значения из переменных окружения
            tokens = self.__substitute_envs(tokens)
            # Извлечем операции присвоения
            assignment, tokens = self.__extract_assignments(tokens)

            # Если строка состоит из операций присвоения, и других токенов нет
            if assignment and not tokens:
                return [assignment]  # Вернем команды присвоения переменных окружения

            # Иначе создадим команду на основе имеющихся токенов, игнорируя присвоения
            command = self.__create_command(tokens)
            commands.append(command)

        return commands

    @staticmethod
    def __tokenize_command(command_string: str) -> list[str]:
        """
        Разделяет строку на команды с учетом кавычек

        :param command_string: строка команды
        :return: список токенов
        """
        special_delimiters = [("'", "'"), ('"', '"')]
        regex_subexpressions = []
        for start_delimiter, end_delimiter in special_delimiters:
            # Регулярное выражение для подстрок, отделенных специальными разделителями
            regex_subexpressions.append(
                r"\S*\{0}[^{1}]*\{1}".format(start_delimiter, end_delimiter)
            )

        # Регулярное выражение для любых не пробельных символов
        tokenizing_regex = "|".join(regex_subexpressions) + r"|\S+"
        tokens = re.findall(tokenizing_regex, command_string)
        return tokens

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
                # Пропускаем токены, начинающиеся в одинарных кавычках
                substituted_tokens.append(token)
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
        # список, хранящий пары аргументов для операций присвоения
        assignments: list[str] = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            # Разделяем присвоение на переменную и значение
            assignment_params = token.split("=", 1)
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

    @staticmethod
    def __strip_single_argument_quotes(argument: str):
        """
        Удаляет кавычки у строкового аргумента, если они есть

        :param argument: строковый аргумент
        :return: строковый аргумент без кавычек
        """
        return argument.strip("'\"")
