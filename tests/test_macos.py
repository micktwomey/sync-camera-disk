import pytest

from sync_camera_disk.macos import (
    parse_plist_output,
    DiskutilList,
    DiskAndPartitions,
    Partition,
)


DROBO_PLIST_OUTPUT = {
    "AllDisks": [
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
    "AllDisksAndPartitions": [
        {
            "Content": "GUID_partition_scheme",
            "DeviceIdentifier": "disk2",
            "OSInternal": False,
            "Partitions": [
                {
                    "Content": "EFI",
                    "DeviceIdentifier": "disk2s1",
                    "DiskUUID": "0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    "Size": 209715200,
                    "VolumeName": "EFI",
                    "VolumeUUID": "0E239BC6-F960-3107-89CF-1C97F78BB46B",
                },
                {
                    "Content": "Apple_APFS",
                    "DeviceIdentifier": "disk2s2",
                    "DiskUUID": "8F050760-6FEF-4491-8D7D-547C6EF0F165",
                    "Size": 2000189177856,
                },
            ],
            "Size": 2000398934016,
        },
        {
            "Content": "GUID_partition_scheme",
            "DeviceIdentifier": "disk4",
            "OSInternal": False,
            "Partitions": [
                {
                    "Content": "EFI",
                    "DeviceIdentifier": "disk4s1",
                    "DiskUUID": "4ABE4C4D-0C31-4997-A7E0-5DACDA41CD05",
                    "Size": 209715200,
                    "VolumeName": "EFI",
                    "VolumeUUID": "85D67001-D93E-3687-A1C2-79D677F0C2E0",
                },
                {
                    "Content": "Apple_HFS",
                    "DeviceIdentifier": "disk4s2",
                    "DiskUUID": "668E9F05-122E-4314-99F5-C80B50FBF53A",
                    "MountPoint": "/Volumes/Drobo",
                    "Size": 17591842070528,
                    "VolumeName": "Drobo",
                    "VolumeUUID": "66EDBE2F-3E53-3EFA-8475-5A97CA67C53B",
                },
            ],
            "Size": 17592186044416,
        },
        {
            "Content": "GUID_partition_scheme",
            "DeviceIdentifier": "disk5",
            "OSInternal": False,
            "Partitions": [
                {
                    "Content": "EFI",
                    "DeviceIdentifier": "disk5s1",
                    "DiskUUID": "EC6E8E47-0EA9-45A8-84DB-46F46BC848CC",
                    "Size": 209715200,
                    "VolumeName": "EFI",
                    "VolumeUUID": "0E239BC6-F960-3107-89CF-1C97F78BB46B",
                },
                {
                    "Content": "Apple_HFS",
                    "DeviceIdentifier": "disk5s2",
                    "DiskUUID": "ED1A6C44-5A98-46B6-846B-10E8E7C610A7",
                    "MountPoint": "/Volumes/Drobo2",
                    "Size": 17591842070528,
                    "VolumeName": "Drobo2",
                    "VolumeUUID": "E8C9AA87-2931-3782-A945-EA3EACEEB5B9",
                },
            ],
            "Size": 17592186044416,
        },
    ],
    "VolumesFromDisks": ["Drobo", "Drobo2"],
    "WholeDisks": ["disk2", "disk4", "disk5"],
}

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

SD_CARD_PLIST_OUTPUT = {
    "AllDisks": ["disk2", "disk2s1", "disk2s2", "disk4", "disk4s1"],
    "AllDisksAndPartitions": [
        {
            "Content": "GUID_partition_scheme",
            "DeviceIdentifier": "disk2",
            "OSInternal": False,
            "Partitions": [
                {
                    "Content": "EFI",
                    "DeviceIdentifier": "disk2s1",
                    "DiskUUID": "0336DDD3-364A-4AFE-B474-5F63EF2B2D21",
                    "Size": 209715200,
                    "VolumeName": "EFI",
                    "VolumeUUID": "0E239BC6-F960-3107-89CF-1C97F78BB46B",
                },
                {
                    "Content": "Apple_APFS",
                    "DeviceIdentifier": "disk2s2",
                    "DiskUUID": "8F050760-6FEF-4491-8D7D-547C6EF0F165",
                    "Size": 2000189177856,
                },
            ],
            "Size": 2000398934016,
        },
        {
            "Content": "FDisk_partition_scheme",
            "DeviceIdentifier": "disk4",
            "OSInternal": False,
            "Partitions": [
                {
                    "Content": "Windows_NTFS",
                    "DeviceIdentifier": "disk4s1",
                    "MountPoint": "/Volumes/DJIMini3Pro",
                    "Size": 124658909184,
                    "VolumeName": "DJIMini3Pro",
                    "VolumeUUID": "3A8C3713-C262-3DB7-8BEC-604865B64393",
                }
            ],
            "Size": 124675686400,
        },
    ],
    "VolumesFromDisks": ["DJIMini3Pro"],
    "WholeDisks": ["disk2", "disk4"],
}

SD_DISKUTIL_LIST = DiskutilList(
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


@pytest.mark.parametrize(
    "plist_output,expected",
    [
        (DROBO_PLIST_OUTPUT, DROBO_DISKUTIL_LIST),
        (SD_CARD_PLIST_OUTPUT, SD_DISKUTIL_LIST),
    ],
    ids=["drobo", "sd_card"],
)
def test_parse_plist_output(plist_output: dict, expected: DiskutilList):
    # Do the dict version first for nicer diffs
    # TODO: find a pydantic mypy plugin for nice diffs
    assert parse_plist_output(plist_output).dict() == expected.dict()
    assert parse_plist_output(plist_output) == expected
