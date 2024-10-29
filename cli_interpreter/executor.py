from io import StringIO

from cli_interpreter.commands.command import Command


class CommandExecutor:
    """
    Принимает последовательность команд от UserInputParser.
    По длине последовательности определяет, какой обработчик должен выполнять обработку команд.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует обработчики команд
        """
        self.sce = SingleCommandExecutor()
        self.pe = PipeExecutor()

    def execute(self, commands: list[Command]) -> None:
        """
        Запуск обработки списка команд.
        Если список единичной длины, передает обработку первого элемента списка в `SingleCommandExecutor`.
        Если длина списка больше одного, то передает список целиком в `PipeExecutor`.
        Иначе должен выбросить исключение
        :param commands: список команд на исполнение
        :return: результат исполнения списка команд
        """
        if len(commands) == 1:
            self.sce.execute(commands[0])
        else:
            self.pe.execute(commands)


class SingleCommandExecutor:
    """
    Обработчик единичной команды
    """

    @staticmethod
    def execute(command: Command) -> None:
        """
        Исполняет переданную на вход команду и возвращает результат её исполнения
        :param command: исполняемая команда
        :return: результат исполнения
        """
        result_code = command.execute()

        if result_code != Command.OK:
            raise RuntimeError(
                f"Command {command} ended with unexpected error code {result_code}"
            )


class PipeExecutor:
    """
    Обработчик нескольких команд, выстроенных в pipeline
    """

    @staticmethod
    def execute(commands: list[Command]) -> None:
        """
        Последовательно исполняет каждую команду, для команд не в начале и не в конце последовательности
        переопределяет потоки ввода и вывода
        :param commands: список команд для исполнения
        :return: результат выполнения последней команды из списка
        """
        if not commands:
            return None

        for i in range(1, len(commands)):
            if not commands[i - 1].output_stream:
                commands[i - 1].output_stream = StringIO()
            commands[i].input_stream = commands[i - 1].output_stream

        for i, command in enumerate(commands):
            is_first = i == 0
            is_last = i == (len(commands) - 1)

            if not is_last:
                # Для не последней команды заводим временной поток ввода/вывода
                command.output_stream = StringIO()

            if not is_first:
                # Для не первой команды
                prev_command = commands[i - 1]
                # Вернемся в начало потока, куда записала результат предыдущая команда
                prev_command.output_stream.seek(0)
                # И укажем его как поток ввода для текущей команды
                command.input_stream = prev_command.output_stream

            # Теперь можно вызывать текущую команду
            result_code = command.execute()

            if result_code != Command.OK:
                # TODO: наверное, поведение должно быть все-таки немного другим
                raise RuntimeError(
                    f"Command {command} ended with unexpected error code {result_code}"
                )

            # Закрываем поток на ввод, который больше не пригодится
            if command.input_stream:
                command.input_stream.close()
