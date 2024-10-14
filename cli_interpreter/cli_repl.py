from cli_interpreter.context import CliContext
from cli_interpreter.executor import CommandExecutor
from cli_interpreter.parser import UserInputParser


class REPL:
    """
    Главный модуль системы и точка входа. Оркеструет работу приложения и реализует Read-Execute-Print Loop.
    """

    def __init__(self):
        """
        Конструктор класса. Инициализирует все необходимые для работы модули
        """
        self.context = CliContext()
        self.parser = UserInputParser(self.context)
        self.executor = CommandExecutor()

    def run(self) -> None:
        """
        Реализует Read-Execute-Print Loop:

        - Считывает строку, поданную пользователем на вход;
        - Передает строку на обработку модулю UserInpurParser;
        - Передает полученную последовательность команд на вход модулю CommandExecutor, который исполняет последовательность команд;
        - Выводит результат исполнения на экран.
        """
        while True:
            user_input = input("Enter command: ")

            # Обработка ошибок при парсинге
            try:
                commands = self.parser.parse(user_input)
            except Exception as e:
                print(f"Error while parsing input: {e}")
                continue

            # Обработка ошибок при выполнении команд
            try:
                commands[0].execute()
            except Exception as e:
                print(f"Error while executing commands: {e}")
                continue


if __name__ == "__main__":
    repl = REPL()
    repl.run()