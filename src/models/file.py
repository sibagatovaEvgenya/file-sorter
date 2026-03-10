# pylint: disable=too-few-public-methods
"""Модуль модели файла"""

import shutil
from pathlib import Path

from src.consts import FILE_TYPE_EXTENSIONS_MAPPING, FileType
from src.models.path import PathModel


class FileModel:
    """
    Модель определенного файла

    Attributes:
        _path (Path): путь к файлу
        _source (Path): путь к папке переноса
    """

    def __init__(self, path: Path, source: Path) -> None:
        self._path: Path = path
        self._source: Path = source

    @property
    def _file_extension(self) -> str:
        """
        Расширение файла в нижнем регистре

        Returns:
            (str): расширение файла

        """
        return self._path.suffix.lower().lstrip(".")

    @property
    def _file_type(self) -> str:
        """
        Тип файла

        Returns:
            (str): тип файла или FileType.OTHER - если не определен

        """
        for file_type_name, extensions in FILE_TYPE_EXTENSIONS_MAPPING.items():
            if self._file_extension in extensions:
                return file_type_name

        return FileType.OTHER

    @property
    def _file_type_folder_name(self) -> str:
        """
        Папка сортировки

        Returns:
            (str): название папки по типу файла

        """
        return self._file_type.title().replace("_", " ")

    @property
    def _folder(self) -> Path:
        """
        Путь до папки сортировки

        Notes:
            Создаст, если ее нет

        Returns:
            (Path): путь до существующей папки сортировки

        """
        path: Path = Path(self._source / self._file_type_folder_name)
        PathModel(path, True).create()

        return path

    def move(self) -> None:
        """
        Перенос папку в каталог по типу

        Examples:
            >>> file: FileModel = FileModel(Path("C:/1/1.jpg"), Path("C:/1"))
            >>> file.move() # Перенесет с "С:/1/Image"

        """
        shutil.move(str(self._path), str(self._folder))
