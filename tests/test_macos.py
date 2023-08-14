import json
import sys
from pathlib import Path
from typing import Any

import pytest

from sync_camera_disk.macos import (
    DiskAndPartitions,
    DiskutilList,
    Partition,
    diskutil_list_physical_external_disks,
    parse_diskutil_output,
)

EXAMPLES = Path(__file__).parent / "examples"

DROBO_PLIST_OUTPUT = json.load((EXAMPLES / "mac_diskutil_drobo.json").open())

DROBO_DISKUTIL_LIST = DiskutilList(
    AllDisks=[
        "disk2",
        "disk2s1",
        "disk2s2",
        "disk4",
        "disk4s1",
        "disk4s2",
        "disk5",
        "disk5s1",
        "disk5s2",
    ],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk4s1",
                    DiskUUID="4ABE4C4D-0C31-4997-A7E0-5DACDA41CD05",
                    Size=209715200,
                    VolumeName="EFI",
                    VolumeUUID="85D67001-D93E-3687-A1C2-79D677F0C2E0",
                ),
                Partition(
                    Content="Apple_HFS",
                    DeviceIdentifier="disk4s2",
                    DiskUUID="668E9F05-122E-4314-99F5-C80B50FBF53A",
                    MountPoint="/Volumes/Drobo",
                    Size=17591842070528,
                    VolumeName="Drobo",
                    VolumeUUID="66EDBE2F-3E53-3EFA-8475-5A97CA67C53B",
                ),
            ],
            Size=17592186044416,
        ),
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk5",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk5s1",
                    DiskUUID="EC6E8E47-0EA9-45A8-84DB-46F46BC848CC",
                    Size=209715200,
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_HFS",
                    DeviceIdentifier="disk5s2",
                    DiskUUID="ED1A6C44-5A98-46B6-846B-10E8E7C610A7",
                    MountPoint="/Volumes/Drobo2",
                    Size=17591842070528,
                    VolumeName="Drobo2",
                    VolumeUUID="E8C9AA87-2931-3782-A945-EA3EACEEB5B9",
                ),
            ],
            Size=17592186044416,
        ),
    ],
    VolumesFromDisks=["Drobo", "Drobo2"],
    WholeDisks=["disk2", "disk4", "disk5"],
)

DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT = json.load(
    (EXAMPLES / "mac_diskutil_dji_osmo_pocket.json").open()
)

DJI_OSMO_POCKET_SD_DISKUTIL_LIST = DiskutilList(
    AllDisks=["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=128026935296,
                    MountPoint="/Volumes/Untitled",
                    VolumeName=None,
                    VolumeUUID="C8BF5026-0077-3F03-AA08-019E0A1DC444",
                ),
            ],
            Size=128043712512,
        ),
    ],
    VolumesFromDisks=[],
    WholeDisks=["disk2", "disk4"],
)

DJI_SD_CARD_PLIST_OUTPUT = json.load((EXAMPLES / "mac_diskutil_dji.json").open())

DJI_SD_DISKUTIL_LIST = DiskutilList(
    AllDisks=["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=124658909184,
                    MountPoint="/Volumes/DJIMini3Pro",
                    VolumeName="DJIMini3Pro",
                    VolumeUUID="3A8C3713-C262-3DB7-8BEC-604865B64393",
                ),
            ],
            Size=124675686400,
        ),
    ],
    VolumesFromDisks=["DJIMini3Pro"],
    WholeDisks=["disk2", "disk4"],
)

# TODO: re-generate without DJI SD plugged in :D
SONY_SD_CARD_PLIST_OUTPUT = json.load(
    (EXAMPLES / "mac_diskutil_sony_a7_iv.json").open()
)

SONY_SD_DISKUTIL_LIST = DiskutilList(
    AllDisks=[
        "disk2",
        "disk2s1",
        "disk2s2",
        "disk4",
        "disk4s1",
        "disk5",
        "disk5s1",
        "disk6",
        "disk6s1",
        "disk7",
        "disk7s1",
    ],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=124658909184,
                    MountPoint="/Volumes/DJIMini3Pro",
                    VolumeName="DJIMini3Pro",
                    VolumeUUID="3A8C3713-C262-3DB7-8BEC-604865B64393",
                ),
            ],
            Size=124675686400,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk5",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk5s1",
                    DiskUUID=None,
                    MountPoint=Path("/Volumes/Untitled"),
                    Size=80009584640,
                    VolumeName=None,
                    VolumeUUID="AB244049-71F0-37A3-9BD7-C0A5085AFE92",
                )
            ],
            Size=80026361856,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk6",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk6s1",
                    DiskUUID=None,
                    MountPoint=Path("/Volumes/Untitled 1"),
                    Size=128291176448,
                    VolumeName=None,
                    VolumeUUID="72F83464-83D9-3C1C-8E25-989D32BF84E5",
                )
            ],
            Size=128307953664,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk7",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="DOS_FAT_32",
                    DeviceIdentifier="disk7s1",
                    DiskUUID=None,
                    MountPoint=Path("/Volumes/PMHOME"),
                    Size=67108352,
                    VolumeName="PMHOME",
                    VolumeUUID="63DD74FE-D4C1-37A5-9B36-913B202618BB",
                )
            ],
            Size=67108864,
        ),
    ],
    VolumesFromDisks=["DJIMini3Pro", "PMHOME"],
    WholeDisks=["disk2", "disk4", "disk5", "disk6", "disk7"],
)

INSTA360_GO_2_PLIST_OUTPUT = json.load(
    (EXAMPLES / "mac_diskutil_insta360_go_2.json").open()
)

INSTA360_GO_2_DISKUTIL_LIST = DiskutilList(
    AllDisks=["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=30798242304,
                    MountPoint="/Volumes/Insta360GO2",
                    VolumeName="Insta360GO2",
                    VolumeUUID="C8BF5026-0077-3F03-AA08-019E0A1DC444",
                ),
            ],
            Size=30802436608,
        ),
    ],
    VolumesFromDisks=["Insta360GO2"],
    WholeDisks=["disk2", "disk4"],
)

INSTA360_ONE_PLIST_OUTPUT = json.load(
    (EXAMPLES / "mac_diskutil_insta360_one.json").open()
)

INSTA360_ONE_DISKUTIL_LIST = DiskutilList(
    AllDisks=["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=125636182016,
                    MountPoint="/Volumes/Untitled",
                    VolumeName=None,
                    VolumeUUID="3A8C3713-C262-3DB7-8BEC-604865B64393",
                ),
            ],
            Size=125652959232,
        ),
    ],
    VolumesFromDisks=[],
    WholeDisks=["disk2", "disk4"],
)


GOPRO_10_PLIST_OUTPUT = json.load((EXAMPLES / "mac_diskutil_gopro_10.json").open())

GOPRO_10_DISKUTIL_LIST = DiskutilList(
    AllDisks=["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    AllDisksAndPartitions=[
        DiskAndPartitions(
            Content="GUID_partition_scheme",
            DeviceIdentifier="disk2",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="EFI",
                    DeviceIdentifier="disk2s1",
                    Size=209715200,
                    DiskUUID="0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    VolumeName="EFI",
                    VolumeUUID="0E239BC6-F960-3107-89CF-1C97F78BB46B",
                ),
                Partition(
                    Content="Apple_APFS",
                    DeviceIdentifier="disk2s2",
                    Size=2000189177856,
                    DiskUUID="8F050760-6FEF-4491-8D7D-547C6EF0F165",
                ),
            ],
            Size=2000398934016,
        ),
        DiskAndPartitions(
            Content="FDisk_partition_scheme",
            DeviceIdentifier="disk4",
            OSInternal=False,
            Partitions=[
                Partition(
                    Content="Windows_NTFS",
                    DeviceIdentifier="disk4s1",
                    Size=511835111424,
                    MountPoint="/Volumes/Untitled",
                    VolumeName=None,
                    VolumeUUID="D4F5EB21-D08D-3267-8F83-F63CDE678B8F",
                ),
            ],
            Size=511868665856,
        ),
    ],
    VolumesFromDisks=[],
    WholeDisks=["disk2", "disk4"],
)


@pytest.mark.parametrize(
    "plist_output,expected",
    [
        (DROBO_PLIST_OUTPUT, DROBO_DISKUTIL_LIST),
        (DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT, DJI_OSMO_POCKET_SD_DISKUTIL_LIST),
        (DJI_SD_CARD_PLIST_OUTPUT, DJI_SD_DISKUTIL_LIST),
        (SONY_SD_CARD_PLIST_OUTPUT, SONY_SD_DISKUTIL_LIST),
        (INSTA360_GO_2_PLIST_OUTPUT, INSTA360_GO_2_DISKUTIL_LIST),
        (INSTA360_ONE_PLIST_OUTPUT, INSTA360_ONE_DISKUTIL_LIST),
        (GOPRO_10_PLIST_OUTPUT, GOPRO_10_DISKUTIL_LIST),
    ],
    ids=[
        "drobo",
        "dji_osmo_pocket_sd_card",
        "dji_sd_card",
        "sony_a7_iv",
        "insta360_go_2",
        "insta360_one",
        "gopro_10",
    ],
)
def test_parse_plist_output(plist_output: Any, expected: DiskutilList) -> None:
    # Do the dict version first for nicer diffs
    # TODO: find a pydantic mypy plugin for nice diffs
    assert parse_diskutil_output(plist_output).dict() == expected.dict()
    assert parse_diskutil_output(plist_output) == expected


@pytest.mark.skipif(sys.platform != "darwin", reason="Only run on Mac")
def test_diskutil_list_physical_external_disks_runs() -> None:
    assert isinstance(diskutil_list_physical_external_disks(), dict)
