import os
import argparse
import sys
from datetime import datetime
from typing import TextIO

from cli_interpreter.commands.command import Command


class LsCommand(Command):
    """
    Команда `ls` — выводит список файлов и директорий в указанной директории.
    Если аргумент не указан, выводит содержимое текущей директории.

    Поддерживаемые опции:
        - `-l` : подробный список с информацией о файлах и директориях
        - `-a` : отображение скрытых файлов (начинающихся с точки)
        - `-t` : сортировка по дате создания (от новых к старым)
    """

    def __init__(self,
                 args: list[str],
                 input_stream: TextIO = None,
                 output_stream: TextIO = None):
        """
        Конструктор инициализирует утилиту для разбора аргументов команды `ls`
        @:param args - аргументы, полученные из пользовательского ввода
        """
        super().__init__(args=args, input_stream=input_stream, output_stream=output_stream)

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "directory",
            type=str,
            nargs="?",
            default=".",
            help="директория для отображения"
        )
        parser.add_argument(
            "-l",
            action="store_true",
            help="использовать длинный формат вывода"
        )
        parser.add_argument(
            "-a",
            action="store_true",
            help="включить скрытые файлы в вывод"
        )
        parser.add_argument(
            "-t",
            action="store_true",
            help="сортировать по дате создания"
        )
        self.arg_parser = parser

    def execute(self) -> int:
        try:
            args = self.arg_parser.parse_args(self.args)
            directory = args.directory
            show_all = args.a
            long_format = args.l
            sort_time = args.t

            try:
                if not os.path.exists(directory):
                    sys.stderr.write(f"ls: cannot access '{directory}': No such file or directory\n")
                    return Command.ILLEGAL_ARGUMENT

                if not os.path.isdir(directory):
                    sys.stderr.write(f"ls: cannot access '{directory}': Not a directory\n")
                    return Command.ILLEGAL_ARGUMENT

                entries = os.listdir(directory)

                if not show_all:
                    # Исключаем скрытые файлы (начинающиеся с точки)
                    entries = [entry for entry in entries if not entry.startswith('.')]
                else:
                    for builtin in [".", ".."]:
                        if builtin not in entries:
                            entries.append(builtin)

                if sort_time:
                    entries.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
                else:
                    entries.sort()

                if long_format:
                    # Длинный формат вывода
                    detailed_entries = [LsCommand._get_detailed_entry(entry, directory) for entry in entries]
                    total_blocks = LsCommand.__calculate_total_blocks(detailed_entries)
                    output = LsCommand.__format_long_output(detailed_entries, total_blocks)
                else:
                    # Краткий формат вывода
                    output = "\n".join(entries)

                self._write_output(output)
                return Command.OK

            except PermissionError:
                sys.stderr.write(f"ls: cannot open directory '{args.directory}': Permission denied\n")
                return Command.ILLEGAL_ARGUMENT
        except Exception as e:
            sys.stderr.write(f"ls: error: {str(e)}\n")
            return Command.ILLEGAL_ARGUMENT

    @staticmethod
    def _get_detailed_entry(entry: str, directory: str) -> dict:
        """Получает подробную информацию о файле или директории."""
        path = os.path.join(directory, entry)
        stats = os.lstat(path)
        if stats:
            return {
                "permissions": LsCommand.__get_permissions(path, stats.st_mode),
                "n_links": stats.st_nlink,
                "owner": LsCommand.__get_owner(stats.st_uid),
                "group": LsCommand.__get_group(stats.st_gid),
                "size": stats.st_size,
                "mtime": LsCommand.__format_time(stats.st_mtime),
                "entry": entry,
                "blocks": getattr(stats, 'st_blocks', 0)
            }

        return {
            "permissions": "?????????",
            "n_links": "?",
            "owner": "?",
            "group": "?",
            "size": "?",
            "mtime": "?",
            "entry": entry,
            "blocks": 0
        }

    @staticmethod
    def __format_long_output(detailed_entries: list, total_blocks: int) -> str:
        """Форматирует длинный вывод с выравниванием столбцов."""
        perms_width = max(len(entry["permissions"]) for entry in detailed_entries) if detailed_entries else 0
        links_width = max(len(str(entry["n_links"])) for entry in detailed_entries) if detailed_entries else 0
        owner_width = max(len(entry["owner"]) for entry in detailed_entries) if detailed_entries else 0
        group_width = max(len(entry["group"]) for entry in detailed_entries) if detailed_entries else 0
        size_width = max(len(str(entry["size"])) for entry in detailed_entries) if detailed_entries else 0
        mtime_width = max(len(entry["mtime"]) for entry in detailed_entries) if detailed_entries else 0

        lines = [
            f"total {total_blocks}"
        ]
        for entry in detailed_entries:
            line = (
                f"{entry['permissions']:<{perms_width}} "
                f"{entry['n_links']:>{links_width}} "
                f"{entry['owner']:<{owner_width}} "
                f"{entry['group']:<{group_width}} "
                f"{entry['size']:>{size_width}} "
                f"{entry['mtime']:<{mtime_width}} "
                f"{entry['entry']}"
            )
            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def __get_permissions(path: str, mode: int):
        """Возвращает строку с правами доступа файла."""
        perms = [
            'r' if mode & 0o400 else '-',
            'w' if mode & 0o200 else '-',
            'x' if mode & 0o100 else '-',
            'r' if mode & 0o040 else '-',
            'w' if mode & 0o020 else '-',
            'x' if mode & 0o010 else '-',
            'r' if mode & 0o004 else '-',
            'w' if mode & 0o002 else '-',
            'x' if mode & 0o001 else '-',
        ]
        file_type = LsCommand.__get_file_type(path)
        return file_type + ''.join(perms)

    @staticmethod
    def __get_file_type(path: str):
        """Определяет тип файла."""
        if os.path.isdir(path):
            return 'd'
        elif os.path.islink(path):
            return 'l'
        else:
            return '-'

    @staticmethod
    def __get_owner(uid):
        """Возвращает имя владельца по UID."""
        try:
            import pwd
            return pwd.getpwuid(uid).pw_name
        except ImportError:
            return str(uid)
        except KeyError:
            return str(uid)

    @staticmethod
    def __get_group(gid):
        """Возвращает имя группы по GID."""
        try:
            import grp
            return grp.getgrgid(gid).gr_name
        except ImportError:
            return str(gid)
        except KeyError:
            return str(gid)

    @staticmethod
    def __format_time(timestamp):
        """Форматирует время последнего изменения."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%b %d %H:%M")

    @staticmethod
    def __calculate_total_blocks(detailed_entries: list) -> int:
        """Вычисляет общее количество блоков для всех записей."""
        return sum(entry["blocks"] for entry in detailed_entries)
