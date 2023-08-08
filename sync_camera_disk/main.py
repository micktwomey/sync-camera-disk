import collections
import json
import logging
import pathlib
from typing import Annotated

import tqdm
import typer
from pydantic_yaml import parse_yaml_file_as
import structlog
import rich.traceback

from sync_camera_disk.config import Config
import sync_camera_disk.disks
from sync_camera_disk import macos
from . import source
from .destination import DatedFolderDestination
from .operation import perform_operation

app = typer.Typer()

LOG: structlog.stdlib.BoundLogger = structlog.get_logger()


@app.command()
def diskutil_list_physical_external_disks() -> None:
    """Run diskutil to list disks and print parsed plist. MacOS only."""
    print(json.dumps(macos.diskutil_list_physical_external_disks()))


@app.command()
def list_disks(
    input: Annotated[typer.FileBinaryRead, typer.Option()] | None = None
) -> None:
    """List all physical external disks"""
    raw_input = input.read() if input is not None else None
    for disk in sync_camera_disk.disks.list_disks(raw_input):
        print(disk.json())


@app.command()
def sync(
    config_path: Annotated[
        pathlib.Path, typer.Argument(help="Path to probes.yml config")
    ],
    dry_run: bool = True,
    verbose: bool = False,
    use_json_logging: bool = False,
) -> None:
    rich.traceback.install(show_locals=True)
    log_level = logging.DEBUG if verbose else logging.INFO
    if use_json_logging:
        # Configure same processor stack as default, minus dev bits
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
        )
    else:
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
        )
    config = parse_yaml_file_as(Config, config_path)
    LOG.debug("config", config=config)

    disks_by_identifer: dict[str, sync_camera_disk.disks.DiskMount] = {
        d.unique_identifier: d for d in sync_camera_disk.disks.list_disks()
    }

    counters: collections.Counter[str] = collections.Counter()

    for sync in tqdm.tqdm(config.syncs, desc="Sync Operations"):
        if sync.source.identifier not in disks_by_identifer:
            continue
        source_disk = disks_by_identifer[sync.source.identifier]
        assert sync.destination.path.is_dir()
        destination = DatedFolderDestination(prefix=sync.destination.path)
        for file_set in tqdm.tqdm(
            list(
                source.enumerate_source_files(
                    source=source_disk, source_type=sync.source.type
                )
            ),
            desc=f"{source_disk.path} -> {sync.destination.path}",
        ):
            LOG.debug("file_set", file_set=file_set)
            for operation in destination.generate_operations(file_set=file_set):
                counters[str(operation.operation)] += 1
                LOG.debug("operation", operation=operation)
                result = perform_operation(operation, dry_run=dry_run)
                LOG.debug("operation result", result=result, success=result.success)
                if not result.success:
                    LOG.info(
                        "perform_operation error",
                        result=result,
                        success=result.success,
                        exception=result.exception,
                        error=result.error,
                    )
                    counters["failure"] += 1
                else:
                    counters["success"] += 1
                if dry_run:
                    counters["dry_run"] += 1
    LOG.info("counters", **counters)
