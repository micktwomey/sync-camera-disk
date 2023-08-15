import pathlib
import sys
from typing import Iterable

import pydantic

from . import macos


class DiskMount(pydantic.BaseModel):
    path: pathlib.Path
    unique_identifier: str
    disk_size: int | None = None
    volume_size: int | None = None
    volume_name: str | None = None
    volume_file_system: str | None = None


def mac_disks_to_disk_mounts(mac_disks: macos.DiskutilList) -> Iterable[DiskMount]:
    for disk_and_partitions in mac_disks.AllDisksAndPartitions:
        for disk in disk_and_partitions.Partitions:
            if disk.MountPoint is not None and disk.VolumeUUID is not None:
                yield DiskMount(
                    path=pathlib.Path(disk.MountPoint),
                    unique_identifier=disk.VolumeUUID.lower(),
                    disk_size=disk_and_partitions.Size,
                    volume_size=disk.Size,
                    volume_name=disk.VolumeName,
                    volume_file_system=disk.Content,
                )
            elif disk.MountPoint is not None and disk.VolumeUUID is None:
                yield DiskMount(
                    path=pathlib.Path(disk.MountPoint),
                    unique_identifier=f"{disk.Content}-{disk_and_partitions.Size}-{disk.Size}",
                    disk_size=disk_and_partitions.Size,
                    volume_size=disk.Size,
                    volume_name=disk.VolumeName,
                    volume_file_system=disk.Content,
                )


def list_disks(input: bytes | None = None) -> Iterable[DiskMount]:
    match sys.platform:
        case "darwin":
            diskutil_disks = (
                macos.DiskutilList.parse_raw(input)
                if input is not None
                else macos.diskutil_list_physical_external_disks()
            )
            mac_disks = macos.parse_diskutil_output(diskutil_disks)
            yield from mac_disks_to_disk_mounts(mac_disks)
        case _:
            raise NotImplementedError(sys.platform)
