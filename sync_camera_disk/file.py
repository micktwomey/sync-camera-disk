import datetime
from pathlib import Path

from pydantic import BaseModel


class File(BaseModel):
    path: Path

    def get_created_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.path.stat().st_ctime)


class FileSet(BaseModel):
    files: list[File]
    stem: str
    prefix: Path
    volume_path: Path  # volume_path / prefix / stem
    volume_identifier: str

    def get_created_datetime(self) -> datetime.datetime:
        return min(f.get_created_datetime() for f in self.files)
