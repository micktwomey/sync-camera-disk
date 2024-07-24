import pathlib
import plistlib
import subprocess
from typing import Any

import pydantic


class Partition(pydantic.BaseModel):
    Content: str
    DeviceIdentifier: str
    DiskUUID: str | None
    Size: int
    VolumeName: str | None
    VolumeUUID: str | None
    MountPoint: pathlib.Path | None


class DiskAndPartitions(pydantic.BaseModel):
    Content: str
    DeviceIdentifier: str
    OSInternal: bool
    Partitions: list[Partition] = pydantic.Field(default_factory=list)
    Size: int


class DiskutilList(pydantic.BaseModel):
    AllDisks: list[str]
    AllDisksAndPartitions: list[DiskAndPartitions]
    VolumesFromDisks: list[str]
    WholeDisks: list[str]


def parse_diskutil_output(plist_output: Any) -> DiskutilList:
    return DiskutilList.parse_obj(plist_output)


def diskutil_list_physical_external_disks() -> Any:
    return plistlib.loads(
        subprocess.run(
            ["diskutil", "list", "-plist", "physical", "external"],
            capture_output=True,
        ).stdout
    )
