import datetime
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel

from .file import FileSet
from .operation import Operation, OperationType


def is_file_identical(a: Path, b: Path) -> bool:
    stat_a = a.stat()
    stat_b = b.stat()
    # Can't use mtime or ctime as these don't accurately copy over.
    # ctime can't be modified easily either.
    # For now assume size and name are enough to test equality
    # TODO: add hash checking!
    return (a.name == b.name) and (stat_a.st_size == stat_b.st_size)


class DatedFolderDestination(BaseModel):
    """Writes files into YYYY-MM-DD folders"""

    prefix: Path

    def get_destination_path(self, path: Path, when: datetime.datetime) -> Path:
        return self.prefix / when.date().isoformat() / path

    def generate_operations(self, file_set: FileSet) -> Iterable[Operation]:
        created = file_set.get_created_datetime()
        for file in file_set.files:
            relative_path = file_set.prefix / file.path.name
            destination_path = self.get_destination_path(
                path=relative_path, when=created
            )
            if not destination_path.exists():
                operation_type = OperationType.copy
            # elif (
            #     destination_path.exists()
            #     and file.path.stat().st_size == destination_path.stat().st_size
            # ):
            #     operation_type = OperationType.copy_stat
            elif destination_path.exists() and is_file_identical(
                file.path, destination_path
            ):
                operation_type = OperationType.identical
            else:
                operation_type = OperationType.unknown
            yield Operation(
                operation=operation_type, source=file.path, destination=destination_path
            )
