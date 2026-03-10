import shutil
from pathlib import Path

from src.consts import FILE_TYPE_EXTENSIONS_MAPPING, FileType
from src.models.path import PathModel


class FileModel:
    def __init__(self, path: Path, source: Path) -> None:
        self._path: Path = path
        self._source: Path = source

    @property
    def _file_extension(self) -> str:
        return self._path.suffix.lower().lstrip(".")

    @property
    def file_type(self) -> str:
        for file_type_name, extensions in FILE_TYPE_EXTENSIONS_MAPPING.items():
            if self._file_extension in extensions:
                return file_type_name

        return FileType.OTHER

    @property
    def file_type_folder_name(self) -> str:
        return self.file_type.title().replace("_", " ")

    @property
    def folder(self) -> Path:
        path: Path = Path(self._source / self.file_type_folder_name)
        PathModel(path, True).create()

        return path

    def move(self) -> None:
        shutil.move(str(self._path), str(self.folder))
