import time
from pathlib import Path

from typer import Typer, Argument, Option

from .console import ConsoleManager
from .models.path import PathModel
from .models.file import FileModel

console_app: Typer = Typer(
    help="Консольная утилита для сортировки файлов по типам в папке"
)

class Sorter:
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
        with self._console_manager.progress as progress:
            task = progress.add_task(
                "[cyan] Сортировка...",
                total=self._path_model.files_count,
                current_file=""

            )

            for i, file in enumerate(self._path_model.files):
                progress.update(
                    task,
                    advance=1,
                    current_file=f"[yellow]{file.name}[/yellow]"
                )
                self._move_file_in_type_folder(file)
                time.sleep(0.5)

                progress.update(
                    task,
                    description=
                    f"[cyan] Сортировка... {i} / {self._path_model.files_count})"

                )


    def _print_start_message(self) -> None:
        self._console_manager.show_welcome()
        self._console_manager.print_log(f"Всего файлов: {self._path_model.files_count}")

    def _move_file_in_type_folder(self, file: Path) -> None:
        model: FileModel = FileModel(file, self._source)
        model.move()

@console_app.command()
def sorter(
        source: Path = Argument(..., help="Путь к папке"),
        silent: bool = Option(False, "--silent", help="Не выводить логи")
) -> None:
    try:
        Sorter(source, silent).sort()
    except SystemError:
        pass
