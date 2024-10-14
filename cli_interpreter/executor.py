from cli_interpreter.commands import Command


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

    def execute(self, commands: list[Command]) -> str:
        """
        Запуск обработки списка команд.
        Если список единичной длины, передает обработку первого элемента списка в `SingleCommandExecutor`.
        Если длина списка больше одного, то передает список целиком в `PipeExecutor`.
        Иначе должен выбросить исключение
        :param commands: список команд на исполнение
        :return: результат исполнения списка команд
        """
        pass


class SingleCommandExecutor:
    """
    Обработчик единичной команды
    """

    def execute(self, command: Command) -> str:
        """
        Исполняет переданную на вход команду и возвращает результат её исполнения
        :param command: исполняемая команда
        :return: результат исполнения
        """
        pass  # TODO: реализовать


class PipeExecutor:
    """
    Обработчик нескольких команд, выстроенных в pipeline
    """

    def execute(self, commands: list[Command]) -> str:
        """
        Последовательно исполняет каждую команду, для команд не в начале и не в конце последовательности
        переопределяет потоки ввода и вывода
        :param commands: список команд для исполнения
        :return: результат выполнения последней команды из списка
        """
        pass
