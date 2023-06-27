from pathlib import Path
from unittest import mock

import pytest

from sync_camera_disk import operation

EXAMPLE_COPY_OPERATION = operation.Operation(
    operation=operation.OperationType.copy,
    source=Path("/source/foo/"),
    destination=Path("/destination/bar"),
)

EXAMPLE_COPY_STAT_OPERATION = operation.Operation(
    operation=operation.OperationType.copy_stat,
    source=Path("/source/foo/"),
    destination=Path("/destination/bar"),
)

EXAMPLE_IDENTICAL_OPERATION = operation.Operation(
    operation=operation.OperationType.identical,
    source=Path("/source/foo/"),
    destination=Path("/destination/bar"),
)

EXAMPLE_UNKNOWN_OPERATION = operation.Operation(
    operation=operation.OperationType.unknown,
    source=Path("/source/foo/"),
    destination=Path("/destination/bar"),
)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            EXAMPLE_COPY_OPERATION,
            operation.OperationResult(
                operation=EXAMPLE_COPY_OPERATION,
                success=True,
                exception=None,
                error=None,
                dry_run=False,
            ),
        ),
        (
            EXAMPLE_COPY_STAT_OPERATION,
            operation.OperationResult(
                operation=EXAMPLE_COPY_STAT_OPERATION,
                success=True,
                exception=None,
                error=None,
                dry_run=False,
            ),
        ),
        (
            EXAMPLE_IDENTICAL_OPERATION,
            operation.OperationResult(
                operation=EXAMPLE_IDENTICAL_OPERATION,
                success=True,
                exception=None,
                error=None,
                dry_run=False,
            ),
        ),
        (
            EXAMPLE_UNKNOWN_OPERATION,
            operation.OperationResult(
                operation=EXAMPLE_UNKNOWN_OPERATION,
                success=False,
                exception="NotImplementedError",
                error=(
                    "operation=<OperationType.unknown: 'unknown'> "
                    "source=PosixPath('/source/foo') "
                    "destination=PosixPath('/destination/bar')"
                ),
                dry_run=False,
            ),
        ),
    ],
    ids=["copy", "copy_stat", "identical", "unknown"],
)
def test_perform_operation(
    input: operation.Operation, expected: operation.OperationResult
) -> None:
    mock_copy = mock.Mock()
    mock_copystat = mock.Mock()
    mock_mkdir = mock.Mock()
    assert (
        operation.perform_operation(
            operation=input,
            dry_run=False,
            copy=mock_copy,
            copystat=mock_copystat,
            mkdir=mock_mkdir,
        )
        == expected
    )
