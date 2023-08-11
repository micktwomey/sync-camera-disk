"""Filters candidate disks configs down to most likely ones

"""
from collections import defaultdict
from typing import Iterable

import structlog

from .config import Config, Sync
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

    In future this might also need to read some files from the disk to match it.
    """
    candidate_syncs_by_identifier: defaultdict[str, list[Sync]] = defaultdict(list)
    for sync in config.syncs:
        candidate_syncs_by_identifier[sync.source.identifier].append(sync)
    LOG.debug("sync candidates", candidates=candidate_syncs_by_identifier)

    disks = list(disks)  # convert to a list to ensure we can iterate over it twice

    candidate_disks_by_identifier: defaultdict[str, list[DiskMount]] = defaultdict(list)
    for disk in disks:
        candidate_disks_by_identifier[disk.unique_identifier].append(disk)
    LOG.debug("disk candidates", candidates=candidate_disks_by_identifier)

    for disk in disks:
        # If we have no candidates continue on
        if disk.unique_identifier not in candidate_syncs_by_identifier:
            LOG.debug(
                "unique_identifier mismatch",
                disk=disk,
                unique_identifier=disk.unique_identifier,
            )
            continue
        syncs: list[Sync] = candidate_syncs_by_identifier[disk.unique_identifier]
        assert syncs  # make sure we have at least one sync
        # If we only have one match return it
        if (
            len(syncs) == 1
            and len(candidate_disks_by_identifier[disk.unique_identifier]) == 1
        ):
            LOG.debug("match", syncs=syncs, disk=disk)
            yield (syncs[0], disk)
            continue

        LOG.debug("attempting best match", syncs=syncs, disk=disk)
        candidates: list[Sync] = []
        for sync in syncs:
            matched = True
            if (sync.source.disk_size is not None) and (
                disk.disk_size != sync.source.disk_size
            ):
                LOG.debug("mismatch", sync=sync, disk=disk, property="disk_size")
                matched = False
            for property in ["volume_size", "volume_name", "volume_file_system"]:
                if (getattr(sync.source, property, None) is not None) and (
                    getattr(disk, property) != getattr(sync.source, property)
                ):
                    LOG.debug("mismatch", sync=sync, disk=disk, property=property)
                    matched = False
            if matched:
                LOG.debug("matched candidate", sync=sync, disk=disk)
                candidates.append(sync)
        if candidates:
            assert len(candidates) == 1  # Don't know what to do with duplicate (yet)
            yield (candidates[0], disk)
