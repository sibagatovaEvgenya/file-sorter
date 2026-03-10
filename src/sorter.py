"""Модуль сортировки файлов"""
import time
from pathlib import Path

from typer import Argument, Option, Typer

from .console import ConsoleManager
from .models.file import FileModel
from .models.path import PathModel

# Экземпляр консольного приложения
console_app: Typer = Typer(help="Консольная утилита для сортировки файлов по типам в папке")


class Sorter:
    """
    Класс для сортировки файлов каталога

    Attributes:
        _source(Path): путь к каталогу сортировки
        _silent(bool): флаг отключения вывода в консоль
        _console_manager(ConsoleManager): инстанс консольного менеджера
        _path_model: (PathModel): Модель каталога

    """
    def __init__(self, source: Path, silent: bool) -> None:
        self._source: Path = source
        self._silent: bool = silent
        self._console_manager: ConsoleManager = ConsoleManager(silent)

        try:
            self._path_model: PathModel = PathModel(self._source)
        except (FileNotFoundError, NotADirectoryError) as exc:
            self._console_manager.print_error(str(exc))
            raise SystemError() from exc

        self._print_start_message()

    def sort(self) -> None:
        """
        Запуск процесса сортировки

        Examples:
             >>> # Сортировка с выводом результата
            >>> sort.inst:Sorter = Sorter(Path(C:/1/2/3), False)
            >>> # Сортировка без вывода результата
            >>> sort.inst:Sorter = Sorter(Path(C:/1/2/3), True)

        """
        with self._console_manager.progress as progress:
            task = progress.add_task("[cyan] Сортировка...", total=self._path_model.files_count, current_file="")

            for i, file in enumerate(self._path_model.files):
                progress.update(task, advance=1, current_file=f"[yellow]{file.name}[/yellow]")
                self._move_file_in_type_folder(file)
                time.sleep(0.5)

                progress.update(task, description=f"[cyan] Сортировка... {i} / {self._path_model.files_count})")

    def _print_start_message(self) -> None:
        """Вывод приветственного сообщениия"""
        self._console_manager.show_welcome()
        self._console_manager.print_log(f"Всего файлов: {self._path_model.files_count}")

    def _move_file_in_type_folder(self, file: Path) -> None:
        """
        Перенести файл в папку типа
        Args:
            file (Path): путь к файлу

        """
        model: FileModel = FileModel(file, self._source)
        model.move()


@console_app.command()
def sorter(
    source: Path = Argument(..., help="Путь к папке"), silent: bool = Option(False, "--silent", help="Не выводить логи")
) -> None:
    """
    Типизированная функция для консольного приложения
    Args:
        source (Path): путь к каталогу сортировки
        silent (bool): флаг отключения вывода в консоль

    """
    try:
        Sorter(source, silent).sort()
    except SystemError:
        pass
