import sys

from cli_interpretator.commands.command import Command


class REPL:
    def pseudo_parser(self, args):
        commands = [arg for arg in args.split() if arg]
        return commands

    def pseudo_execute(self, args):
        if args[0] == "echo":
            print(*args[1:])
            return 0
        elif args[0] == "exit":
            return 1
        else:
            print("Unknown command")
            return 0

    def run(self):
        while True:
            user_input = input("Enter command: ")
            # commands = Parser(user_input).parse
            commands = self.pseudo_parser(user_input)

            # command_handler = Command(commands)
            # result = command_handler.execute()
            result = self.pseudo_execute(commands)
            if result == 1:
                return


if __name__ == "__main__":
    repl = REPL()
    repl.run()