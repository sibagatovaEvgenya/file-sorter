from pathlib import Path


class FileModel:
    def __init__(self, path: Path, source: Path) -> None:
        self._path: Path = path
        self._source: Path = source
        
    @property
    def _file_extention(selfself, self=None) -> str:
        return self._path.suffix.lower().lstrip(".")