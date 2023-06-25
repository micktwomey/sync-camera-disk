import enum
from pathlib import Path
import shutil
from typing import Iterable

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


def perform_operation(operation: Operation, dry_run: bool = True) -> OperationResult:
    try:
        match operation.operation:
            case OperationType.copy:
                if not dry_run:
                    operation.destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(operation.source, operation.destination)
            case OperationType.identical:
                pass
            case OperationType.copy_stat:
                if not dry_run:
                    shutil.copystat(operation.source, operation.destination)
            case _:
                raise NotImplementedError(operation)
    except Exception as e:
        return OperationResult(
            operation=operation,
            success=False,
            exception=str(type(e)),
            error=str(e),
            dry_run=dry_run,
        )
    return OperationResult(operation=operation, success=True, dry_run=dry_run)
