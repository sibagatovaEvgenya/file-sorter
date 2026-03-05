from pathlib import Path
from typing import Generator, Any


class PathModel:
    def __init__(self, path: Path, skip_check: bool = False) -> None:
        self._path: Path = path

        if not skip_check:
            self._check_exist()

    @property
    def files_count(self) -> str:
        file_count: int = 0

        for item in self._path.iterdir():
            if item.is_file():
                file_count += 1

        return file_count

    @property
    def files(self) -> Generator[Path, Any, None]:
        for item in self._path.iterdir():
            if item.is_file():
                yield item

    def create(self) -> None:
        self._path.mkdir(parents=True, exist_ok=True)


    def _check_exist(self) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f'Папка {self._path} не существует')

        if not self._path.is_dir():
            raise NotADirectoryError(f'Путь {self._path} не папка')

