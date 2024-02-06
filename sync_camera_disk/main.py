import collections
import json
import logging
import sys
from pathlib import Path
from typing import Annotated

import rich
import rich.traceback
import structlog
import typer
import xdg_base_dirs
from pydantic_yaml import parse_yaml_file_as, to_yaml_str
from rich.progress import Progress

import sync_camera_disk.disks
from sync_camera_disk import macos
from sync_camera_disk.config import Config, Destination, Source, SourceType, Sync

from . import source
from .destination import DatedFolderDestination
from .filter_disks import filter_disks_to_syncs
from .operation import perform_operation

app = typer.Typer()

LOG: structlog.stdlib.BoundLogger = structlog.get_logger()

# Note that this will lookup the config path so will vary from run to run
# depending on env vars.
DEFAULT_CONFIG_PATH = (
    xdg_base_dirs.xdg_config_home() / "sync-camera-disk" / "config.yaml"
)


@app.command()
def diskutil_list_physical_external_disks() -> None:
    """Run diskutil to list disks and print parsed plist. MacOS only."""
    rich.print_json(json.dumps(macos.diskutil_list_physical_external_disks()))


@app.command()
def list_disks(
    input: Annotated[typer.FileBinaryRead, typer.Option()] | None = None,
) -> None:
    """List all physical external disks"""
    raw_input = input.read() if input is not None else None
    for disk in sync_camera_disk.disks.list_disks(raw_input):
        rich.print_json(disk.json())


@app.command()
def generate_config(
    input: Annotated[typer.FileBinaryRead, typer.Option()] | None = None,
    config_path: Annotated[
        Path, typer.Argument(help="Path to probes.yml config")
    ] = DEFAULT_CONFIG_PATH,
    overwrite: bool = False,
) -> None:
    """Generate a sample config for disks seen on the system

    Tries to generate the most specific config possible to make identification
    more reliable.

    Note that you still have to fill in details such as the disk type and
    destination paths.
    """
    sample_config = Config(syncs=[])

    raw_input = input.read() if input is not None else None
    for disk in sync_camera_disk.disks.list_disks(raw_input):
        sample_config.syncs.append(
            Sync(
                destination=Destination(path=Path("/tmp/example")),
                source=Source(
                    identifier=disk.unique_identifier,
                    type=SourceType.unknown,
                    description=f"External disk mounted at {disk.path}",
                    disk_size=disk.disk_size,
                    volume_file_system=disk.volume_file_system,
                    volume_size=disk.volume_size,
                    volume_name=disk.volume_name,
                    platform=sys.platform,
                ),
            )
        )
    config = to_yaml_str(sample_config)
    rich.print(config)

    if overwrite and config_path.is_file():
        LOG.info(f"Overwriting {config_path}")
    elif config_path.is_file():
        LOG.info(f"Not overwriting existing {config_path}")

    if (not config_path.is_file()) or overwrite:
        LOG.info(f"Writing to {config_path}")
        config_path.parent.mkdir(exist_ok=True, parents=True)
        with config_path.open("w") as fp:
            fp.write(config)


@app.command()
def show_syncs(
    config_path: Annotated[
        Path, typer.Argument(help="Path to probes.yml config")
    ] = DEFAULT_CONFIG_PATH,
) -> None:
    """Show which sync configurations will be used for detected disks"""
    config = parse_yaml_file_as(Config, config_path)
    LOG.debug("config", config=config)

    syncs = list(
        filter_disks_to_syncs(config=config, disks=sync_camera_disk.disks.list_disks())
    )
    for sync, source_disk in syncs:
        rich.print("\n".join(("---", to_yaml_str(source_disk), to_yaml_str(sync))))


@app.command()
def sync(
    config_path: Annotated[
        Path, typer.Argument(help="Path to probes.yml config")
    ] = DEFAULT_CONFIG_PATH,
    dry_run: bool = True,
) -> None:
    """Sync files from disks to configured destinations"""
    config = parse_yaml_file_as(Config, config_path)
    LOG.debug("config", config=config)

    counters: collections.Counter[str] = collections.Counter()

    syncs = list(
        filter_disks_to_syncs(config=config, disks=sync_camera_disk.disks.list_disks())
    )
    with Progress() as progress:
        syncs_task = progress.add_task("Syncs", total=len(syncs))
        for sync, source_disk in syncs:
            assert sync.destination.path.is_dir()
            destination = DatedFolderDestination(prefix=sync.destination.path)
            file_sets = list(
                source.enumerate_source_files(
                    source=source_disk, source_type=sync.source.type
                )
            )
            operations_task = progress.add_task(
                f"{source_disk.path} -> {sync.destination.path}",
                total=sum(len(file_set.files) for file_set in file_sets),
            )
            for file_set in file_sets:
                LOG.debug("file_set", file_set=file_set)
                for operation in destination.generate_operations(file_set=file_set):
                    counters[str(operation.operation)] += 1
                    LOG.debug("operation", operation=operation)
                    LOG.info(
                        operation.operation,
                        type=sync.source.type,
                        source=operation.source,
                        destination=operation.destination,
                    )
                    result = perform_operation(operation, dry_run=dry_run)
                    LOG.debug("operation result", result=result, success=result.success)
                    if not result.success:
                        LOG.error(
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
                    progress.update(operations_task, advance=1)
            progress.update(syncs_task, advance=1)
    LOG.info("counters", **counters)


@app.callback()
def main(
    verbose: bool = True,
    debug: bool = False,
    quiet: bool = False,
    use_json_logging: bool = False,
) -> None:
    rich.traceback.install(show_locals=True)
    log_level = logging.INFO if verbose else logging.WARNING
    log_level = logging.DEBUG if debug else log_level
    log_level = logging.WARNING if quiet else log_level
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
