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


def test_copy_recursively() -> None:
    """Ensure copying child folders under a prefix does the right thing"""
    mock_copy = mock.Mock()
    mock_copystat = mock.Mock()
    mock_mkdir = mock.Mock()
    test_operation = operation.Operation(
        source=Path("/Volumes/ATEM/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4"),
        destination=Path(
            "/Volumes/Cameras/ATEM SDI Extreme ISO/2024-09-16/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4"
        ),
        operation=operation.OperationType.copy,
    )

    assert operation.perform_operation(
        operation=test_operation,
        dry_run=False,
        copy=mock_copy,
        copystat=mock_copystat,
        mkdir=mock_mkdir,
    ) == operation.OperationResult(
        dry_run=False,
        error=None,
        exception=None,
        operation=test_operation,
        success=True,
    )
    mock_mkdir.assert_called_once_with(
        Path(
            "/Volumes/Cameras/ATEM SDI Extreme ISO/2024-09-16/PyLadies/Video ISO Files"
        )
    )
    mock_copy.assert_called_once_with(
        Path("/Volumes/ATEM/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4"),
        Path(
            "/Volumes/Cameras/ATEM SDI Extreme ISO/2024-09-16/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4"
        ),
    )
