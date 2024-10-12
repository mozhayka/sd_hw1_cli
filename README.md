# Задача про CLI

## Задача:

#### Реализовать простой интерпретатор командной строки, поддерживающий команды: 
- cat [FILE] — вывести на экран содержимое файла 
- echo — вывести на экран свой аргумент (или аргументы) 
- wc [FILE] — вывести количество строк, слов и байт в файле 
- pwd — распечатать текущую директорию 
- exit — выйти из интерпретатора

- Должны поддерживаться одинарные и двойные кавычки (full and weak quoting) 
- Окружение (команды вида “имя=значение”), оператор $ 
- Вызов внешней программы через Process (или его аналоги) 
- Пайплайны (оператор “|”) 

## Состав команды

- Могилевский Матвей
- Можаев Андрей
- Шадрин Михаил
- Яценко Кирилл

## Архитектура

![image](https://github.com/user-attachments/assets/16a35445-2814-46f1-939f-d7b7d1412355)

- CliInterpretator - принимает аргументы командной строки, вызывает UserInpurParser, затем вызывает ComandExecutor от массива распаршенных команд
- UserInpurParser - принимает на вход строку, разбивает на пайпы, совершает подстановку всех аргументов, возвращает массив команд
- ComandExecutor - принимает на вход массив команд, для каждой отдельной команды вызывает command, передавая при необходимости вывод предыдущей на вход следующей
- Command - принимает на вход команду и аргументы и исполняет ее в зависимости от типа
- CliContext - работа с переменными окружения

Точка входа - CliInterpretator. При запуске пользователь вводит команды, которые обрабатываются в бесконечном цикле REPL. Завершение программы происходит, когда пользователь вводит команду exit

## Parser
- Принимает на вход строку, которую ввел пользователь.
- Определяет и запоминает переменые окружения, а также выполняет подстановку. Для хранения, модификации и подстановки используются методы setEnv и getEnv в UserInputParser
- Обрабатывает пайплайны, разбивая на команды по оператору `|`

### Строки

#### Зарезервированные символы: $, |

- Weak Quoting (Слабое квотирование)\
Используется двойными кавычками ("). Переменные окружения всё ещё могут быть подставлены внутри двойных кавычек. Например, "Hello, $USER" будет заменено на Hello, username, если переменная USER задана.

- Full Quoting (Полное квотирование)\
Используется одинарными кавычками ('). Все символы внутри одинарных кавычек воспринимаются буквально. Подстановка переменных и интерпретация специальных символов не производится. Это позволяет сохранять точное содержание строки без замены.

#### Переменные окружения
Название переменной окружения обычно состоит из следующих символов:
- Буквы: Латинские буквы от A до Z (как заглавные, так и строчные — однако, в Unix-подобных системах обычно используются заглавные).
- Цифры: От 0 до 9. Однако цифры не могут стоять на первом месте в имени переменной.
- Знак подчеркивания (_): Часто используется для разделения слов в названии переменной.

Дополнительно:
* Имя переменной окружения не должно начинаться с цифры. Оно должно начинаться с буквы или знака подчеркивания
* Создание Переменной окружения возможно только отдельной командой 
* Ее нельзя создать в рамках вызова pipe

## Command
- Для каждой команды свой класс (CatCommand, EchoCommand, WcCommand, PwdCommand, ExitCommand, UnknownCommand), унаследованные от базового класса Command, имеющие перегруженный метод execute
- Создается экземпляр класса, которому передаются аргументы, а также потоки ввода и вывода, затем запуск метода execute

### Обработка пайплайнов:
Если встречается оператор пайплайна `|`, оркестратор понимает, что надо организовать вызов нескольких команд последовательно, передавая результат выполнения одной команды другой. Для этого stdout предыдущей команды передается как stdin следующей. Переопределять stdin и stdout можно только у первой и последней команд в пайпе соответственно

В этом случае команды помещаются в PipelineManager, который создает конвейер потоков (пайп) между соответствующими командами:
```
PipelineManager pipeline = new PipelineManager();
pipeline.addCommand(echoCommand);
pipeline.addCommand(wcCommand);
pipeline.execute();
```

### Исполнение встроенных и внешних команд:
После разбиения на команды и анализа, какие из них встроенные, а какие внешние:
- Если команда встроенная (например, echo, cat, wc), оркестратор напрямую вызывает ее исполнение, передавая ей параметры.
``` Command result = echoCommand.execute(stdin, stdout); ```

- Если команда внешняя (например, системная утилита, как ls или grep), оркестратор запускает её как внешний процесс с помощью, например, fork

