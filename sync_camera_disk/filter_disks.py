"""Filters candidate disks configs down to most likely ones"""

from typing import Iterable

import structlog

from .config import Config, MatchType, Sync
from .disks import DiskMount

LOG: structlog.stdlib.BoundLogger = structlog.get_logger()


def filter_disks_to_syncs(
    config: Config,
    disks: Iterable[DiskMount],
) -> Iterable[tuple[Sync, DiskMount]]:
    """Finds the best matching sync config for each disk present

    Normally the volume UUID should be unique enough but in some cases the volume
    UUID is identical between disks (and manufacturers) so we need to use secondary
    characteristics to get a best match.

    Uses match_on config to determine which properties to match on.

    In future this might also need to read some files from the disk to match it.
    """

    disks = list(disks)  # convert to a list to ensure we can iterate over it twice

    for sync in config.syncs:
        matched_disks: list[DiskMount] = []
        for disk in disks:
            matches: list[bool] = []
            LOG.debug(
                "Attempting to match",
                disk=disk,
                match_on=sync.source.match_on,
                sync=sync,
            )
            for expected_match in sync.source.match_on:
                match expected_match:
                    case MatchType.identifier:
                        matches.append(disk.unique_identifier == sync.source.identifier)
                    case MatchType.disk_size:
                        matches.append(disk.disk_size == sync.source.disk_size)
                    case MatchType.volume_size:
                        matches.append(disk.volume_size == sync.source.volume_size)
                    case MatchType.volume_file_system:
                        matches.append(
                            disk.volume_file_system == sync.source.volume_file_system
                        )
            if len(matches) == len(sync.source.match_on) and all(matches):
                matched_disks.append(disk)
        assert len(matched_disks) <= 1, (len(matched_disks), matched_disks, sync)
        if matched_disks:
            yield (sync, matched_disks[0])
