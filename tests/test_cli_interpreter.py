import unittest
from unittest.mock import patch
from io import StringIO
from cli_interpreter.cli_interpreter import REPL  # Убедитесь, что импорт правильный


class TestREPL(unittest.TestCase):

    @patch('builtins.input', side_effect=['echo 1', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run(self, mock_stdout, mock_input):
        repl = REPL()
        repl.run()  # Запуск REPL.

        # Проверяем, что вывод содержит '1'
        output = mock_stdout.getvalue()
        self.assertIn('1', output)
        self.assertIn('Enter command: ', output)  # Убедимся, что программа запрашивала ввод
