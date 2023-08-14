import enum
import shutil
from pathlib import Path
from typing import Callable

from pydantic import BaseModel


class OperationType(enum.StrEnum):
    copy = "copy"
    identical = "identical"
    copy_stat = "copy_stat"
    unknown = "unknown"


class Operation(BaseModel):
    operation: OperationType
    source: Path
    destination: Path


class OperationResult(BaseModel):
    operation: Operation
    success: bool
    exception: str | None
    error: str | None
    dry_run: bool


def mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def perform_operation(
    operation: Operation,
    dry_run: bool = True,
    mkdir: Callable[[Path], None] = mkdir,
    copy: Callable[[str | Path, str | Path], None] = shutil.copy2,
    copystat: Callable[[str | Path, str | Path], None] = shutil.copystat,
) -> OperationResult:
    try:
        match operation.operation:
            case OperationType.copy:
                if not dry_run:
                    mkdir(operation.destination.parent)
                    copy(operation.source, operation.destination)
            case OperationType.identical:
                pass
            case OperationType.copy_stat:
                if not dry_run:
                    copystat(operation.source, operation.destination)
            case _:
                raise NotImplementedError(operation)
    except Exception as e:
        return OperationResult(
            operation=operation,
            success=False,
            exception=e.__class__.__name__,
            error=str(e),
            dry_run=dry_run,
        )
    return OperationResult(operation=operation, success=True, dry_run=dry_run)
